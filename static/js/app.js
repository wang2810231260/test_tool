// Main Vue App
new Vue({
    el: '#app',
    components: {
        'order-management': httpVueLoader('/static/components/OrderManagement.vue'),
        'product-management': httpVueLoader('/static/components/ProductManagement.vue'),
        'payout-payment': httpVueLoader('/static/components/payoutPayment.vue'),
        'coupon-template': httpVueLoader('/static/components/Coupon.vue'),
        'user-coupon': httpVueLoader('/static/components/CouponUser.vue'),
        'activity-management': httpVueLoader('/static/components/Active.vue')
    },
    data: {
        activeTab: 'order-generation',
        orderSubmenuOpen: true,
        couponSubmenuOpen: true,
        // sysCodes will be passed from global window variable injected by Flask
        sysCodes: window.SYS_CODES || ['ToCredi'],
        toasts: []
    },
    methods: {
        switchTab(tabId) {
            this.activeTab = tabId;
        },
        toggleOrderSubmenu() {
            this.orderSubmenuOpen = !this.orderSubmenuOpen;
        },
        toggleCouponSubmenu() {
            this.couponSubmenuOpen = !this.couponSubmenuOpen;
        },
        showToast(message, type = 'info') {
            const id = Date.now();
            this.toasts.push({ id, message, type });

            // Auto remove after 3 seconds
            setTimeout(() => {
                this.toasts = this.toasts.filter(t => t.id !== id);
            }, 3000);
        }
    }
});

// Global fetch override to handle token expiration (401)
const originalFetch = window.fetch;
window.fetch = async function (...args) {
    const response = await originalFetch(...args);
    const clonedResponse = response.clone();
    try {
        const data = await clonedResponse.json();
        const code = data.code || (data.data && data.data.code);
        if (code === 401 || (code === 404 && data.msg === 'token过期')) {
            window.location.href = '/logout';
        }
    } catch (e) {
        // Ignore JSON parsing errors
    }
    return response;
};
