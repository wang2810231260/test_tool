<template>
    <section id="payout-payment" class="content-section active">
        <h1 class="section-title">放还款</h1>
        <div class="form-container">
            <p>放款</p>
            <div class="form-group">
                <label>选择 APP</label>
                <div class="input-container">
                    <select v-model="selectedApp" class="select-input">
                        <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>放款状态</label>
                <div class="input-container">
                    <select v-model="payoutStatus" class="select-input">
                        <option v-for="status in statusList" :key="status" :value="status">{{ status }}</option>
                    </select>
                    <input type="text" v-model="payoutMobile" class="text-input" placeholder="请输入手机号" maxlength="10">
                    <button :disabled="generating" class="action-btn" @click="payout">执行</button>
                </div>
            </div>
        </div>

        <div class="form-container" style='margin-top: 20px;'>
            <p>还款</p>
            <p style="color: red;">确保已生成流水</p>
            <div class="form-group">
                <label>选择 APP</label>
                <div class="input-container">
                    <select v-model="selectedApp" class="select-input">
                        <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>还款状态</label>
                <div class="input-container">
                    <select v-model="paymentStatus" class="select-input">
                        <option v-for="status in statusList" :key="status" :value="status">{{ status }}</option>
                    </select>
                    <input type="text" v-model="paymentMobile" class="text-input" placeholder="请输入手机号" maxlength="10">
                    <button :disabled="generating" class="action-btn" @click="payment">执行</button>
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
            statusList: ['SUCCESS', 'FAILED'],
            payoutStatus: 'SUCCESS',
            paymentStatus: 'SUCCESS',
            generating: false,
            paymentMobile: '',
            payoutMobile: '',
        };
    },
    methods: {
        async payout() {
            if (!this.selectedApp || !this.payoutStatus) {
                this.$root.showToast('请选择 APP 和放款状态', 'warning');
                return;
            }
            this.generating = true;
            try {
                const res = await fetch(`/generate_payout?status=${this.payoutStatus}&app=${this.selectedApp}&mobile=${this.payoutMobile}`);
                const data = await res.json();
                this.$root.showToast(data.msg || '执行完毕', data.code === 200 ? 'success' : 'error');
            } catch (error) {
                this.$root.showToast('执行失败', 'error');
            } finally {
                this.generating = false;
            }
        },
        async payment() {
            if (!this.selectedApp || !this.paymentStatus) {
                this.$root.showToast('请选择 APP 和还款状态', 'warning');
                return;
            }
            this.generating = true;
            try {
                const res = await fetch(`/generate_payment?status=${this.paymentStatus}&app=${this.selectedApp}&mobile=${this.paymentMobile}`);
                const data = await res.json();
                this.$root.showToast(data.msg || '执行完毕', data.code === 200 ? 'success' : 'error');
            } catch (error) {
                this.$root.showToast('执行失败', 'error');
            } finally {
                this.generating = false;
            }
        }
    }
};
</script>
