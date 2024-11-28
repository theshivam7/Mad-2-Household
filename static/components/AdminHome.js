export default {
    template: `
    <div class="home-container">
        <div class="content-wrapper">
            <div class="welcome-section">
                <h1 class="title">Welcome Admin</h1>
                <p class="subtitle">Manage Your Services</p>
            </div>

            <div class="action-section">
                <router-link to="/create-service" class="create-btn">
                    <i class="fas fa-plus-circle"></i> New Service
                </router-link>
            </div>

            <div class="services-card">
                <div class="card-header">
                    <div class="header-grid">
                        <div class="header-item">
                            <i class="fas fa-hashtag"></i> ID
                        </div>
                        <div class="header-item">
                            <i class="fas fa-tools"></i> Service Name
                        </div>
                        <div class="header-item">
                            <i class="fas fa-rupee-sign"></i> Base Price
                        </div>
                        <div class="header-item">
                            <i class="fas fa-cogs"></i> Action
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <!-- Service items will be rendered here -->
                </div>
            </div>

            <div class="export-section" v-if="isWaiting">
                <div class="loading-spinner">
                    <i class="fas fa-spinner fa-spin"></i> Processing...
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            isWaiting: false
        }
    },
    methods: {
        async download_csv() {
            this.isWaiting = true
            try {
                const res = await fetch('/download-csv')
                const data = await res.json()
                if (res.ok) {
                    const taskId = data['task-id']
                    const intv = setInterval(async () => {
                        const csv_res = await fetch(`/get-csv/${taskId}`)
                        if(csv_res.ok){
                            this.isWaiting = false
                            clearInterval(intv)
                            window.location.href = `/get-csv/${taskId}`
                        }
                    }, 1000)
                }
            } catch (err) {
                this.isWaiting = false
                console.error('Download failed:', err)
            }
        }
    }
}