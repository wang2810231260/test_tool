<template>
    <section id="payout-payment" class="content-section active">
        <h1 class="section-title">活动管理</h1>
        <div class="form-order-info">
            <div class="form-group">
                <label>选择 APP</label>
                <div class="input-container">
                    <select v-model="selectedApp" class="select-input">
                        <option v-for="code in sysCodes" :key="code" :value="code">{{ code }}</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>审核中弹窗重制</label>
                <div class="input-container">
                    <p style="margin: 0; font-weight: 600;">+54</p>
                    <input type="text" v-model="pendingMobile" class="text-input" placeholder="请输入手机号" maxlength="10">
                    <button class="action-btn" @click="reset1">重置</button>
                </div>
            </div>
            <div class="form-group">
                <label>好评弹窗重置</label>
                <div class="input-container">
                    <p style="margin: 0; font-weight: 600;">+54</p>
                    <input type="text" v-model="ratingMobile" class="text-input" placeholder="请输入手机号" maxlength="10">
                    <button class="action-btn" @click="reset2">重置</button>
                </div>
            </div>
            <div class="form-group">
                <label>促确认弹窗确认</label>
                <div class="input-container">
                    <p style="margin: 0; font-weight: 600;">+54</p>
                    <input type="text" v-model="comfirmMobile" class="text-input" placeholder="请输入手机号" maxlength="10">
                    <button class="action-btn" @click="reset3">重置</button>
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
            pendingMobile: "",
            ratingMobile: "",
            comfirmMobile: ""
        };
    },
    methods: {
        async reset1() {
            if (this.pendingMobile == "") {
                this.$root.showToast("请输入手机号", "error");
                return;
            }
            try {
                const request_data = {
                    app: this.selectedApp,
                    mobile: this.pendingMobile
                }
                const res = await fetch(`/reset1`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(request_data)
                });
                const data = await res.json();
                if (data.code === 200) {
                    this.$root.showToast('重置成功', 'success');
                } else {
                    this.$root.showToast(data.msg, 'error');
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('失败', 'error');
            }




        },
        async reset2() {
            if (this.ratingMobile == "") {
                this.$root.showToast("请输入手机号", "error");
                return;
            }
            try {
                const request_data = {
                    app: this.selectedApp,
                    mobile: this.ratingMobile
                }
                const res = await fetch(`/reset2`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(request_data)
                });
                const data = await res.json();
                if (data.code === 200) {
                    this.$root.showToast('重置成功', 'success');
                } else {
                    this.$root.showToast(data.msg, 'error');
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('失败', 'error');
            }

        },
        async reset3() {
            if (this.pendingMobile == "") {
                this.$root.showToast("请输入手机号", "error");
                return;
            }
            try {
                const request_data = {
                    app: this.selectedApp,
                    mobile: this.pendingMobile
                }
                const res = await fetch(`/reset3`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(request_data)
                });
                const data = await res.json();
                if (data.code === 200) {
                    this.$root.showToast('重置成功', 'success');
                } else {
                    this.$root.showToast(data.msg, 'error');
                }
            } catch (error) {
                console.error(error);
                this.$root.showToast('失败', 'error');
            }
        }



    }
}
</script>
