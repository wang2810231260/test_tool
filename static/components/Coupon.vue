<template>
    <section id="coupon-template-section" class="content-section active">
        <h1 class="section-title">优惠券模版</h1>

        <div class="result-wrapper" style="margin-top: 20px; display: block; overflow-x: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <button class="action-btn" @click="openAddModal">新增优惠券</button>
            </div>
            <table class="coupon-table">
                <thead>
                    <tr>
                        <th>优惠券名称</th>
                        <th>类型</th>
                        <th>金额</th>
                        <th>剩余数量</th>
                        <th>有效期</th>
                        <th>APP</th>
                        <th>是否可用</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in couponTemplateList" :key="index">
                        <td>{{ item.name }}</td>
                        <td>{{ item.couponType == 1 ? '减免卷' : (item.couponType == 4 ? '提额卷' : '延期券') }}</td>
                        <td>{{ item.distributeAmount }}</td>
                        <td>{{ item.surplusCount }}</td>
                        <td>{{ item.validDays }} 天</td>
                        <td>{{ item.sysCode }}</td>
                        <td>
                            <span
                                :class="['status-badge', item.isAvailable == 1 ? 'status-active' : 'status-inactive']">
                                {{ item.isAvailable == 1 ? '可用' : '禁用' }}
                            </span>
                        </td>
                        <td>
                            <button class="edit-btn" @click="editItem(item, index)">编辑</button>
                            <button class="delete-btn" @click="deleteItem(item.id)">删除</button>
                        </td>
                    </tr>
                    <tr v-if="couponTemplateList.length === 0">
                        <td colspan="8" style="text-align: center; color: #9ca3af; padding: 20px;">暂无优惠券模版数据</td>
                    </tr>
                </tbody>
            </table>
            <div v-if="showEditModal" class="modal-overlay">
                <div class="modal-content">
                    <header class="modal-header">
                        <h3>{{ isEditMode ? '编辑优惠券模版' : '新增优惠券模版' }}</h3>
                        <button class="close-x" @click="closeEdit">×</button>
                    </header>
                    <div class="modal-body">
                        <div class="form-group horizontal">
                            <label>优惠券类型</label>
                            <div class="radio-group">
                                <label class="radio-item">
                                    <input type="radio" :value="1" v-model="editingItem.couponType"
                                        @change="handleTypeChange"> 减免卷
                                </label>
                                <label class="radio-item">
                                    <input type="radio" :value="4" v-model="editingItem.couponType"
                                        @change="handleTypeChange"> 提额卷
                                </label>
                                <label class="radio-item">
                                    <input type="radio" :value="2" v-model="editingItem.couponType"
                                        @change="handleTypeChange"> 延期券
                                </label>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>优惠券名称</label>
                            <input type="text" v-model="editingItem.name" class="text-input" placeholder="请输入优惠券名称">
                        </div>
                        <div class="form-group">
                            <label>优惠券金额</label>
                            <input type="number" v-model.number="editingItem.distributeAmount" class="text-input"
                                placeholder="请输入金额">
                        </div>
                        <div class="form-group">
                            <label>数量</label>
                            <input type="number" v-model.number="editingItem.count" class="text-input"
                                placeholder="请输入发放数量">
                        </div>
                        <div class="form-group">
                            <label>有效天数</label>
                            <input type="number" v-model.number="editingItem.validDays" class="text-input"
                                placeholder="请输入有效天数">
                        </div>
                        <div class="form-group">
                            <label>优惠券App展示名称</label>
                            <input type="text" v-model="editingItem.showName" class="text-input"
                                placeholder="请输入App展示名称">
                        </div>
                        <div class="form-group">
                            <label>App项目</label>
                            <select v-model="editingItem.sysCode" class="select-input">
                                <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                            </select>
                        </div>
                    </div>
                    <footer class="modal-footer">
                        <button class="secondary-btn" @click="closeEdit">关闭</button>
                        <button class="action-btn" @click="saveEdit">{{ isEditMode ? '保存' : '新增' }}</button>
                    </footer>
                </div>
            </div>

            <!-- 分页控制 -->
            <div class="pagination-container" v-if="totalPages > 1">
                <div class="pagination-info">
                    共 {{ totalItems }} 条数据，第 {{ currentPage }}/{{ totalPages }} 页
                </div>
                <div class="pagination-buttons">
                    <button class="pag-btn" :disabled="currentPage === 1"
                        @click="changePage(currentPage - 1)">上一页</button>
                    <button v-for="page in visiblePages" :key="page"
                        :class="['pag-btn', { active: page === currentPage }]" @click="changePage(page)">
                        {{ page }}
                    </button>
                    <button class="pag-btn" :disabled="currentPage === totalPages"
                        @click="changePage(currentPage + 1)">下一页</button>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
module.exports = {
    props: ['sysCodes', 'activeTab'],
    data() {
        return {
            couponTemplateList: [],
            currentPage: 1,
            pageSize: 10,
            totalItems: 0,
            totalPages: 0,
            showEditModal: false,
            isEditMode: false,
            editingItem: {}
        };
    },
    computed: {
        visiblePages() {
            const pages = [];
            const start = Math.max(1, this.currentPage - 2);
            const end = Math.min(this.totalPages, start + 4);
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        }
    },

    watch: {
        activeTab(newTab) {
            if (newTab === 'coupon-template') {
                this.getCouponTemplate();
            }
        }
    },
    methods: {
        async getCouponTemplate() {
            try {
                const res = await fetch(`/get_coupon_template?current=${this.currentPage}&size=${this.pageSize}`);
                const data = await res.json();

                if (data.code === 200 || data.data) {
                    this.couponTemplateList = data.data.content
                    this.totalItems = data.data.totalElements
                    this.totalPages = Math.ceil(this.totalItems / this.pageSize);
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('获取优惠券模版失败', 'error');
            }
        },
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.getCouponTemplate();
            }
        },
        async editItem(item, index) {
            this.isEditMode = true
            this.editingItem = {
                couponType: item.couponType,
                name: item.name,
                distributeAmount: item.distributeAmount,
                count: item.surplusCount,
                validDays: item.validDays,
                showName: item.appName,
                sysCode: item.sysCode,
                id: item.id
            };
            this.showEditModal = true

        },
        async deleteItem(id) {
            // this.$root.showToast('删除功能尚未实现', 'warning');
            // console.log(id)
            try {
                const res = await fetch(`/delete_coupon?id=${id}`);
                const data = await res.json();

                if (data.code === 200 || data.data) {
                    this.$root.showToast('删除成功！', 'success');
                    this.getCouponTemplate(); // 刷新列表
                } else {
                    this.$root.showToast(data.msg || '操作失败', 'error');
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('删除失败', 'error');
            }
        },
        openAddModal() {
            this.isEditMode = false;
            this.editingItem = {
                couponType: 1,
                name: '',
                distributeAmount: null,
                count: null,
                validDays: null,
                showName: 'Reduce el monto total por pagar según el valor del cupón.',
                sysCode: this.sysCodes[0]
            };
            this.showEditModal = true;
        },
        handleTypeChange() {
            const typeMap = {
                1: 'Reduce el monto total por pagar según el valor del cupón.',
                4: 'Aumenta el monto disponible de su préstamo según el valor del cupón.',
                2: 'Extiende el plazo de su préstamo según los días indicados en el cupón.'
            };
            this.editingItem.showName = typeMap[this.editingItem.couponType] || '';
        },
        closeEdit() {
            this.showEditModal = false;
        },
        async saveEdit() {
            if (!this.editingItem.name || !this.editingItem.distributeAmount || !this.editingItem.count || !this.editingItem.validDays) {
                this.$root.showToast('请完整填写优惠券信息', 'warning');
                return;
            }
            if (this.isEditMode) {
                try {
                    const res = await fetch('/edit_coupon', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(this.editingItem)
                    });
                    const data = await res.json();
                    console.log(data)
                    if (data.code === 200) {
                        this.$root.showToast('编辑成功！', 'success');
                        this.showEditModal = false;
                        this.getCouponTemplate(); // 刷新列表
                    } else {
                        this.$root.showToast(data.msg || '编辑失败', 'error');
                    }

                } catch (error) {
                    console.error(error);
                    this.$root.showToast('编辑失败', 'error');
                }
            } else {
                try {
                    const res = await fetch('/add_coupon', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(this.editingItem)
                    });
                    const data = await res.json();
                    console.log(data)
                    if (data.code === 200) {
                        this.$root.showToast('新增成功！', 'success');
                        this.showEditModal = false;
                        this.getCouponTemplate(); // 刷新列表
                    } else {
                        this.$root.showToast(data.msg || '操作失败', 'error');
                    }

                } catch (error) {
                    console.error(error);
                    this.$root.showToast('保存失败', 'error');
                }
            }


        }

    }
};
</script>

<style scoped>
.coupon-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    background: white;
    font-size: 0.9em;
}

.coupon-table th,
.coupon-table td {
    border: 1px solid #e5e7eb;
    padding: 12px 15px;
    text-align: left;
}

.coupon-table th {
    background-color: #f9fafb;
    font-weight: 600;
    color: #374151;
}

.status-badge {
    padding: 4px 8px;
    border-radius: 9999px;
    font-size: 0.75em;
    font-weight: 500;
}

.status-active {
    background-color: #d1fae5;
    color: #065f46;
}

.status-inactive {
    background-color: #fee2e2;
    color: #991b1b;
}

.edit-btn,
.delete-btn {
    padding: 4px 8px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.85em;
    margin-right: 5px;
    color: white;
}

.edit-btn {
    background-color: #3b82f6;
}

.delete-btn {
    background-color: #ef4444;
}

.pagination-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding: 10px 0;
}

.pagination-info {
    font-size: 0.9em;
    color: #6b7280;
}

.pagination-buttons {
    display: flex;
    gap: 5px;
}

.pag-btn {
    padding: 5px 12px;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9em;
    transition: all 0.2s;
}

.pag-btn:hover:not(:disabled) {
    background-color: #f3f4f6;
    border-color: #9ca3af;
}

.pag-btn.active {
    background-color: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.pag-btn:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}

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
    width: 520px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.modal-header h3 {
    margin: 0;
    font-size: 1.2em;
}

.close-x {
    border: none;
    background: none;
    font-size: 1.5em;
    cursor: pointer;
    color: #6b7280;
}

.modal-body .form-group {
    margin-bottom: 15px;
}

.form-group.horizontal {
    display: flex;
    align-items: center;
    gap: 15px;
}

.form-group.horizontal label {
    margin-bottom: 0;
    white-space: nowrap;
    min-width: 80px;
}

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

.radio-group {
    display: flex;
    flex-direction: row;
    gap: 15px;
    padding: 10px 0;
    justify-content: space-between;
    flex-wrap: nowrap;
}

.radio-item {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 0.95em;
    color: #374151;
    white-space: nowrap;
}

.radio-item input[type="radio"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
    margin: 0;
}
</style>
