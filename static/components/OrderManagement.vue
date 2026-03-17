<template>
    <section id="order-generation" class="content-section active">
        <h1 class="section-title">订单生成</h1>
        <h1 class="section-title">test111111</h1>

        <div class="form-container">
            <div class="form-group">
                <label>选择 APP</label>
                <div class="input-container">
                    <select v-model="selectedApp" class="select-input">
                        <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>订单状态</label>
                <div class="input-container">
                    <select v-model="orderStatus" class="select-input">
                        <option value="pending">待申请</option>
                        <option value="pending_liveness">待申请(活体未做)</option>
                        <option value="not_pass">审核拒绝</option>
                        <option value="calculated">首贷试算</option>
                        <option value="shipped">放款中</option>
                        <option value="payout_failed">放款失败</option>
                        <option value="paid">还款页面</option>
                        <option value="reloan_trial">复贷试算</option>
                    </select>
                    <button :disabled="generating" class="action-btn" @click="generateOrder">生成订单</button>
                </div>
            </div>

            <div v-if="generating" class="progress-wrapper" style="display: block;">
                <div class="progress-label">
                    <span>{{ progressText }}</span>
                    <span>{{ progressPercentage }}%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" :style="{ width: progressPercentage + '%' }"></div>
                </div>
            </div>

            <div v-if="showResult" class="result-wrapper" style="display: block;">
                <label style="font-weight: 600; display: block; margin-bottom: 8px;">生成手机号</label>
                <input type="text" v-model="generatedMobile" class="text-input" :placeholder="resultPlaceholder"
                    :readonly="!isSuccess">
                <label style="font-weight: 600; display: block; margin-bottom: 8px; margin-top: 10px;">用户id</label>
                <input type="text" v-model="generatedUserId" class="text-input" placeholder="等待生成..."
                    :readonly="!isSuccess">
            </div>
        </div>

        <div class="form-infomation">
            <div class="form-group">
                <label>获取可用cuit</label>
                <div class="input-container">
                    <input type="text" v-model="cuit" class="text-input" readonly>
                    <button :disabled="fetchingCuit" class="action-btn" @click="getCuit">获取</button>
                </div>
            </div>
            <div class="form-group">
                <label>获取可用银行卡号</label>
                <div class="input-container">
                    <input type="text" v-model="bankNo" class="text-input" readonly>
                    <button :disabled="fetchingBankNo" class="action-btn" @click="getBankNo">获取</button>
                </div>
            </div>
        </div>

        <div class="form-order-info">
            <div class="form-group">
                <label>选择 APP</label>
                <div class="input-container">
                    <select v-model="selectedAppInvalid" class="select-input">
                        <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>当前订单置为失效</label>
                <div class="input-container">
                    <p style="margin: 0; font-weight: 600;">+54</p>
                    <input type="text" v-model="invalidOrderMobile" class="text-input" placeholder="请输入手机号"
                        maxlength="10">
                    <button :disabled="invalidatingOrder" class="action-btn" @click="orderInvalid">失效</button>
                </div>
            </div>
            <div class="form-group">
                <label>当前用户活体置为失效</label>
                <div class="input-container">
                    <p style="margin: 0; font-weight: 600;">+54</p>
                    <input type="text" v-model="invalidLivenessMobile" class="text-input" placeholder="请输入手机号"
                        maxlength="10">
                    <button :disabled="invalidatingLiveness" class="action-btn" @click="livenessInvalid">失效</button>
                </div>
            </div>
            <div class="form-group">
                <label>当前订单置为审核中</label>
                <div class="input-container">
                    <p style="margin: 0; font-weight: 600;">+54</p>
                    <input type="text" v-model="orderToPendingMobile" class="text-input" placeholder="请输入手机号"
                        maxlength="10">
                    <button :disabled="orderToPending" class="action-btn" @click="orderInvalidToPending">置为审核</button>
                </div>
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
            orderStatus: 'pending',
            generating: false,
            progressText: '',
            progressPercentage: 0,
            showResult: false,
            generatedMobile: '',
            generatedUserId: '',
            resultPlaceholder: '等待生成...',
            isSuccess: false,

            cuit: '',
            bankNo: '',
            fetchingCuit: false,
            fetchingBankNo: false,

            selectedAppInvalid: this.sysCodes[0],
            invalidOrderMobile: '',
            invalidLivenessMobile: '',
            orderToPendingMobile: '',
            invalidatingOrder: false,
            invalidatingLiveness: false,
            orderToPending: false
        };
    },
    methods: {
        generateOrder() {
            if (!this.orderStatus) {
                this.$root.showToast("请先选择一个订单状态！", "warning");
                return;
            }
            if (!this.selectedApp) {
                this.$root.showToast("请先选择一个APP！", "warning");
                return;
            }

            this.generating = true;
            this.showResult = false;
            this.progressPercentage = 0;
            this.progressText = '连接服务中...';

            let totalFiles = 1;
            let completedFiles = 0;

            const eventSource = new EventSource(`/generate_order_tests?status=${encodeURIComponent(this.orderStatus)}&app=${encodeURIComponent(this.selectedApp)}`);

            eventSource.onmessage = (event) => {
                const data = event.data;
                if (!data.startsWith('>>>')) {
                    console.log(data);
                    return;
                }

                if (data.startsWith('>>>ERROR::')) {
                    this.$root.showToast('Error: ' + data.substring(10), 'error');
                    eventSource.close();
                    this.generating = false;
                    return;
                }

                if (data === '>>>TOKEN_EXPIRED') {
                    eventSource.close();
                    this.generating = false;
                    this.$root.showToast('管理员 Token 已失效，即将退出登录...', 'error');
                    setTimeout(() => { window.location.href = '/logout'; }, 1500);
                    return;
                }

                if (data.startsWith('>>>TOTAL_FILES:::')) {
                    totalFiles = parseInt(data.replace('>>>TOTAL_FILES:::', '').trim());
                    this.progressText = '订单正在生成中...';
                    return;
                }

                if (data.startsWith('>>>FILE_COMPLETE:::')) {
                    completedFiles++;
                    this.progressPercentage = Math.min(Math.round((completedFiles / totalFiles) * 100), 95);
                    return;
                }

                if (data.startsWith('>>>TEST_EXECUTION_COMPLETE::')) {
                    eventSource.close();
                    this.progressPercentage = 100;
                    this.progressText = '执行完毕！';

                    let finalMobile = "";
                    let finalUserId = "";
                    if (data.includes('SUCCESS:::')) {
                        const parts = data.split(':::');
                        if (parts.length > 1) finalMobile = parts[1].trim();
                        if (parts.length > 2) finalUserId = parts[2].trim();
                    }

                    setTimeout(() => {
                        this.generating = false;
                        this.showResult = true;
                        this.isSuccess = data.includes('SUCCESS');
                        if (this.isSuccess) {
                            this.generatedMobile = finalMobile;
                            this.generatedUserId = finalUserId;
                            this.resultPlaceholder = finalMobile ? "已填入" : "请在此录入数据";
                        } else {
                            this.resultPlaceholder = "执行失败，检查F12";
                        }
                    }, 800);
                }
            };

            eventSource.onerror = (e) => {
                console.error("SSE failed:", e);
                eventSource.close();
                this.generating = false;
                this.$root.showToast('连接服务器中断', 'error');
            };
        },
        async getCuit() {
            this.fetchingCuit = true;
            try {
                const res = await fetch('/generate_cuit');
                const data = await res.json();
                this.cuit = data.cuit;
                this.$root.showToast("获取 CUIT 成功", "success");
            } catch (e) {
                this.$root.showToast("获取 CUIT 失败", "error");
            } finally {
                this.fetchingCuit = false;
            }
        },
        async getBankNo() {
            this.fetchingBankNo = true;
            try {
                const res = await fetch('/generate_cbu');
                const data = await res.json();
                this.bankNo = data.cbu;
                this.$root.showToast("获取银行卡号成功", "success");
            } catch (e) {
                this.$root.showToast("获取银行卡号失败", "error");
            } finally {
                this.fetchingBankNo = false;
            }
        },
        async orderInvalid() {
            if (!this.invalidOrderMobile) {
                alert("请输入手机号！");
                return;
            }
            this.invalidatingOrder = true;
            try {
                const res = await fetch(`/order_invalid?mobile=${this.invalidOrderMobile}&app=${this.selectedAppInvalid}`);
                const data = await res.json();
                this.$root.showToast(data.msg || "操作成功", "success");
            } catch (e) {
                this.$root.showToast("操作失败", "error");
            } finally {
                this.invalidatingOrder = false;
            }
        },
        async livenessInvalid() {
            if (!this.invalidLivenessMobile) {
                alert("请输入手机号！");
                return;
            }
            this.invalidatingLiveness = true;
            try {
                const res = await fetch(`/liveness_invalid?mobile=${this.invalidLivenessMobile}&app=${this.selectedAppInvalid}`);
                const data = await res.json();
                this.$root.showToast(data.msg || "操作成功", "success");
            } catch (e) {
                this.$root.showToast("操作失败", "error");
            } finally {
                this.invalidatingLiveness = false;
            }
        },
        async orderInvalidToPending() {
            if (!this.orderToPendingMobile) {
                alert("请输入手机号！");
                return;
            }
            this.orderToPending = true;
            try {
                const res = await fetch(`/order_invalid_to_pending?mobile=${this.orderToPendingMobile}&app=${this.selectedAppInvalid}`);
                const data = await res.json();
                this.$root.showToast(data.msg || "操作成功", "success");
            } catch (e) {
                this.$root.showToast("操作失败", "error");
            } finally {
                this.orderToPending = false;
            }
        }
    }
};
</script>
