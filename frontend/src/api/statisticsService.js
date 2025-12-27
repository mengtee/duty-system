import apiClient from './client';

export default {
    // Get duty statistics
    getDutyStatistics(startDate = null, endDate = null) {
        return apiClient.get('/api/statistics/duty', {
            params: { start_date: startDate, end_date: endDate }
        });
    },

    // Get workload statistics
    getWorkload(startDate = null, endDate = null) {
        return apiClient.get('/api/statistics/workload', {
            params: { start_date: startDate, end_date: endDate }
        });
    },

    // Get shift distribution
    getShiftDistribution(startDate = null, endDate = null) {
        return apiClient.get('/api/statistics/shifts', {
            params: { start_date: startDate, end_date: endDate }
        });
    },

    // Get comprehensive report
    getComprehensiveReport(startDate = null, endDate = null) {
        return apiClient.get('/api/statistics/comprehensive', {
            params: { start_date: startDate, end_date: endDate }
        });
    }
};
