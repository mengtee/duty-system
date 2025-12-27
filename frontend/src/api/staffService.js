import apiClient from './client';

export default {
    // Get all staff
    getAllStaff(includeInactive = false) {
        return apiClient.get('/api/staff', {
            params: { include_inactive: includeInactive }
        });
    },

    // Get staff by ID
    getStaffById(id) {
        return apiClient.get(`/api/staff/${id}`);
    },

    // Create staff
    createStaff(staffData) {
        return apiClient.post('/api/staff/', staffData);
    },

    // Delete staff
    deleteStaff(id) {
        return apiClient.delete(`/api/staff/${id}`);
    },

    // Get staff statistics
    getStatistics() {
        return apiClient.get('/api/staff/statistics/summary');
    }
};
