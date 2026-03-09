<template>
    <section id="payout-payment" class="content-section active">
        <h1 class="section-title">产品列表</h1>
        <div class="form-container">
            <div class="form-group">
                <label>APP</label>
                <div class="input-container">
                    <select v-model="selectedApp" class="select-input">
                        <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>手机号</label>
                <div class="input-container">
                    <input type="text" v-model="mobile" class="text-input" placeholder="请输入手机号" maxlength="10">
                    <button :disabled="generating" class="action-btn" @click="get_product_list">查找产品</button>
                </div>
            </div>
        </div>

        <!-- 产品列表展示 (表格化) -->
        <div v-if="productList.length > 0" class="result-wrapper" style="margin-top: 20px; display: block; overflow-x: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h2 style="font-size: 1.1em; margin: 0;">产品列表详情</h2>
                <button class="action-btn" @click="openAddModal">新增产品</button>
            </div>
            <table class="product-table">
                <thead>
                    <tr>
                        <th>天数</th>
                        <th>最小放款金额</th>
                        <th>最大放款金额</th>
                        <th>期数</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in productList" :key="index">
                        <td>{{ item.term }} 天</td>
                        <td>{{ item.quota_min }}</td>
                        <td>{{ item.quota }}</td>
                        <td>{{ item.stage_num }} 期</td>
                        <td>
                            <button class="edit-btn" @click="editItem(item, index)">编辑</button>
                            <button class="delete-btn" @click="deleteItem(index)">删除</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 编辑/新增 弹窗 -->
        <div v-if="showEditModal" class="modal-overlay">
            <div class="modal-content">
                <header class="modal-header">
                    <h3>{{ isEditMode ? '编辑产品信息' : '新增产品信息' }}</h3>
                    <button class="close-x" @click="closeEdit">×</button>
                </header>
                <div class="modal-body">
                    <h2 v-if="!isEditMode" style="color: red;font-size: 12px;"> 多期产品只支持:14,16,18,20,22天,单期产品只支持:首贷:8-15天,复贷:8-22天</h2>
                    <div class="form-group">
                        <label>天数</label>
                        <input type="number" v-model.number="editingItem.term" class="text-input" @input="syncSubPeriod">
                    </div>
                    <div class="form-group">
                        <label>最小放款金额(最小2w)</label>
                        <input type="number" v-model.number="editingItem.quota_min" class="text-input">
                    </div>
                    <div class="form-group">
                        <label>最大放款金额(最大60w)</label>
                        <input type="number" v-model.number="editingItem.quota" class="text-input">
                    </div>
                    <div class="form-group" v-if="!isEditMode">
                        <label>期数</label>
                        <input type="number" v-model.number="editingItem.stage_num" class="text-input" @input="syncSubPeriod">
                    </div>
                </div>
                <footer class="modal-footer">
                    <button class="secondary-btn" @click="closeEdit">关闭</button>
                    <button class="action-btn" @click="saveEdit">{{ isEditMode ? '保存' : '新增' }}</button>
                </footer>
            </div>
        </div>
    </section>
</template>

<script>
module.exports = {
    props: ['sysCodes'],
    data() {
        return {
            selectedApp: this.sysCodes[0],
            generating: false,
            mobile: '',
            productList: [],
            // 窗体相关
            showEditModal: false,
            isEditMode: false,
            editingItem: {},
            editingIndex: -1
        };
    },
    methods: {
        async get_product_list() {
            if (!this.selectedApp || !this.mobile) {
                this.$root.showToast('请选择 APP 和手机号', 'error');
                return;
            }
            this.generating = true;
            try {
                const res = await fetch(`/get_product_list?app=${this.selectedApp}&mobile=${this.mobile}`);
                const data = await res.json();
                if (data.code === 200 && data.data.length > 0) {
                    let rawStageInfo = data.data[0].stage_info;
                    let stageInfo = [];
                    
                    try {
                        stageInfo = typeof rawStageInfo === 'string' ? JSON.parse(rawStageInfo) : rawStageInfo;
                    } catch (e) {
                        console.error('JSON 解析失败:', e);
                        stageInfo = [];
                    }

                    this.productList = Array.isArray(stageInfo) ? stageInfo : [stageInfo];
                } else {
                    this.$root.showToast(data.msg || '未找到产品信息', 'error');
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('获取产品列表失败', 'error');
            } finally {
                this.generating = false;
            }
        },
        openAddModal() {
            this.isEditMode = false;
            this.editingIndex = -1;
            // 初始化内容为空白，让用户自行输入
            this.editingItem = {
                term: null,
                quota_min: null,
                quota: null,
                stage_num: 1, // 默认为 1 期
                fees: 0,
                stage_detail: []
            };
            this.showEditModal = true;
        },
        editItem(item, index) {
            this.isEditMode = true;
            this.editingIndex = index;
            this.editingItem = JSON.parse(JSON.stringify(item));
            this.showEditModal = true;
        },
        async deleteItem(index) {
            if (confirm('确定要删除这项产品配置吗？')) {
                const oldList = [...this.productList];
                this.productList.splice(index, 1);
                try {
                    const res = await fetch(`/update_product_list?app=${this.selectedApp}&mobile=${this.mobile}&stage_info=${encodeURIComponent(JSON.stringify(this.productList))}`);
                    const data = await res.json();
                    if (data.code === 200) {
                        this.$root.showToast('删除成功！', 'success');
                    } else {
                        this.$root.showToast(data.msg, 'error');
                        this.productList = oldList; // 恢复
                    }
                } catch (error) {
                    console.error(error);
                    this.$root.showToast('删除失败', 'error');
                    this.productList = oldList; // 恢复
                }
            }
        },
        async saveEdit() {
            // 参数校验
            if (this.editingItem.quota_min < 20000) {
                this.$root.showToast('最小放款金额不能小于 20,000', 'warning');
                return;
            }
            if (this.editingItem.quota > 600000) {
                this.$root.showToast('最大放款金额不能大于 600,000', 'warning');
                return;
            }
            if (this.editingItem.quota_min > this.editingItem.quota) {
                this.$root.showToast('最小放款金额不能大于最大放款金额', 'warning');
                return;
            }
            if(this.editingItem.stage_num>2){
                this.$root.showToast('期数不能大于2', 'warning');
                return
            }
            if(this.editingItem.stage_num==2){
                if(this.editingItem.term<14){
                    this.$root.showToast('多期产品天数不能小于14', 'warning');
                    return
                }
            }
            if(this.editingItem.stage_num==1){
                if(this.editingItem.term<8){
                    this.$root.showToast('单期产品天数不能小于8', 'warning');
                    return
                }
            }

            const oldList = JSON.parse(JSON.stringify(this.productList));
            
            if (this.isEditMode) {
                // 编辑模式：替换
                this.productList.splice(this.editingIndex, 1, this.editingItem);
            } else {
                // 新增模式：追加
                this.productList.push(this.editingItem);
            }

            try {
                const res = await fetch(`/update_product_list?app=${this.selectedApp}&mobile=${this.mobile}&stage_info=${encodeURIComponent(JSON.stringify(this.productList))}`);
                const data = await res.json();
                if (data.code === 200) {
                    this.$root.showToast(this.isEditMode ? '修改成功！' : '新增成功！', 'success');
                    this.showEditModal = false;
                } else {
                    this.$root.showToast(data.msg, 'error');
                    this.productList = oldList; // 还原数据
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('保存失败', 'error');
                this.productList = oldList; // 还原数据
            }
        },
        async syncSubPeriod() {
            const term = this.editingItem.term || 0;
            const stageNum = this.editingItem.stage_num || 1;

            if (stageNum === 2) {
                const subPeriod = Math.floor(term / 2);
                this.editingItem.stage_detail = [
                    { sub_percentage: 5000, sub_period: subPeriod ,current_num:1},
                    { sub_percentage: 5000, sub_period: subPeriod ,current_num:2}
                ];
            } else {
                // 默认为 1 期
                this.editingItem.stage_detail = [
                    { sub_percentage: 10000, sub_period: term }
                ];
            }
        },
        async closeEdit() {
            this.showEditModal = false;
        }
    }
}
</script>

<style scoped>
.product-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    background: white;
    font-size: 0.9em;
}

.product-table th, .product-table td {
    border: 1px solid #e5e7eb;
    padding: 12px 15px;
    text-align: left;
}

.product-table th {
    background-color: #f9fafb;
    font-weight: 600;
    color: #374151;
}

.product-table tr:hover {
    background-color: #f3f4f6;
}

.edit-btn, .delete-btn {
    padding: 4px 8px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.85em;
    margin-right: 5px;
}

.edit-btn { background-color: #3b82f6; color: white; }
.delete-btn { background-color: #ef4444; color: white; }

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 24px;
    border-radius: 12px;
    width: 450px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.modal-header h3 { margin: 0; font-size: 1.2em; }
.close-x { border: none; background: none; font-size: 1.5em; cursor: pointer; color: #6b7280; }

.modal-body .form-group { margin-bottom: 15px; }

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.secondary-btn {
    padding: 8px 16px;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 6px;
    cursor: pointer;
}
</style>

