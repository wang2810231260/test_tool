<template>
    <div>
        <section id="payout-payment" class="content-section active">
            <h1 class="section-title">用户优惠券</h1>
        </section>

        <div class="result-wrapper" style="margin-top: 20px; display: block; overflow-x: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <button class="action-btn" @click="openAddModal">新增用户优惠券</button>
                <h1>11111</h1>
            </div>
            <table class="coupon-table">
                <thead>
                    <tr>
                        <th>客户id</th>
                        <th>优惠券类型</th>
                        <th>状态</th>
                        <th>金额</th>
                        <th>是否已读 </th>
                        <th>APP</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in couponUserList" :key="index">
                        <td>{{ item.accountId }}</td>
                        <td>{{ item.couponType == 1 ? '减免卷' : (item.couponType == 4 ? '提额卷' : '延期券') }}</td>
                        <td>{{ item.status == 1 ? '可用' : (item.status == 2 ? '冻结' : (item.couponType == 3 ? '已使用' :
                            '已过期')) }} <button v-if="item.status == 1" class="edit-btn"
                                @click="expiredCoupon(item.id)">过期</button></td>
                        <td>{{ item.sendAmount }}</td>
                        <td>{{ item.isRead == 1 ? '已读' : '未读' }} <button v-if="(item.status == 1) && (item.isRead == 1)"
                                class="edit-btn" @click="toRead(item.id)">变成可读</button></td>
                        <td>{{ item.sysCode }}</td>
                        <td>
                            <button class="delete-btn" @click="deleteItem(item.id)">删除</button>
                        </td>
                    </tr>
                    <tr v-if="couponUserList.length === 0">
                        <td colspan="8" style="text-align: center; color: #9ca3af; padding: 20px;">暂无优惠券模版数据</td>
                    </tr>
                </tbody>
            </table>
            <div class="modal-overlay" v-if="showEditModal">
                <div class="modal-content">
                    <header class="modal-header">
                        <h3>新增用户优惠券</h3>
                        <button class="close-x" @click="closeEdit">×</button>
                    </header>
                    <div class="modal-body">
                    </div>
                    <div class="form-group">
                        <label>App</label>
                        <select v-model="sysCode" class="select-input" @change="getCouponList(sysCode)">
                            <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>优惠券</label>
                        <select v-model="selectedCoupon" class="select-input">
                            <option v-for="coupon in couponList" :key="coupon.id" :value="coupon">{{ coupon.name }}
                            </option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>客户手机号</label>
                        <input type="text" v-model="mobile" class="text-input" placeholder="请输入用户手机号" maxlength="10">
                    </div>
                    <footer class="modal-footer">
                        <button class="secondary-btn" @click="closeEdit">关闭</button>
                        <button class="action-btn" @click="saveEdit">新增</button>
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
    </div>
</template>

<script>

module.exports = {
    props: ['sysCodes', 'activeTab'],
    data() {
        return {
            sysCode: "",
            couponUserList: [],
            currentPage: 1,
            pageSize: 10,
            totalItems: 0,
            totalPages: 0,
            mobile: "",
            couponList: [],
            selectedCoupon: null,
            showEditModal: false,


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
            if (newTab === 'user-coupon') {
                this.getCouponUser();
            }
        }
    },
    methods: {
        async getCouponUser() {
            try {
                const res = await fetch(`/get_coupon_user?current=${this.currentPage}&size=${this.pageSize}`);
                const data = await res.json();

                if (data.code === 200 || data.data) {
                    this.couponUserList = data.data.content
                    this.totalItems = data.data.totalElements
                    this.totalPages = Math.ceil(this.totalItems / this.pageSize);
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('获取用户优惠券失败', 'error');
            }
        },
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.getCouponUser();
            }
        },
        async openAddModal() {
            this.showEditModal = true;
        },
        async toRead(id) {
            try {

                const res = await fetch(`/to_read?id=${id}`);
                const data = await res.json();
                if (data.code === 200 || data.data) {
                    this.getCouponUser();
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('标记已读失败', 'error');
            }
        },
        async deleteItem(id) {

            try {
                const res = await fetch(`/delete_coupon_user?id=${id}`);
                const data = await res.json();
                if (data.code === 200 || data.data) {
                    this.getCouponUser();
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('删除失败', 'error');
            }
        },
        async closeEdit() {
            this.showEditModal = false

        },
        async saveEdit() {
            if (!this.sysCode || !this.mobile || !this.selectedCoupon) {
                this.$root.showToast('请填写完整信息', 'error');
            }
            try {
                const res = await fetch(`/add_coupon_user?sysCode=${this.sysCode}&mobile=${this.mobile}&couponId=${this.selectedCoupon.id}`);
                const data = await res.json();
                if (data.code === 200 || data.data) {
                    this.$root.showToast('新增成功', 'success');
                    this.getCouponUser();
                    this.showEditModal = false
                } else {
                    this.$root.showToast(data.msg, 'error');
                }
            } catch (error) {
                this.$root.showToast(error.msg, 'error');
            }
        },
        async getCouponList(sysCode) {
            try {
                const res = await fetch(`/get_coupon_list?sysCode=${sysCode}`);
                const data = await res.json();
                if (data.code === 200 || data.data) {
                    this.couponList = data.data
                }

            } catch {
                this.$root.showToast('获取优惠券列表失败', 'error');
            }
        },
        async expiredCoupon(id) {
            try {
                const res = await fetch(`/expired_coupon?id=${id}`);
                const data = await res.json();
                if (data.code === 200 || data.data) {
                    this.$root.showToast("操作成功", "success")
                    this.getCouponUser();
                } else {
                    this.$root.showToast(data.msg, "error")
                }

            } catch {
                this.$root.showToast("操作失败", "error")
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
