import apiClient from './client';

export default {
    // Create schedule
    createSchedule(scheduleData) {
        return apiClient.post('/api/schedules/', scheduleData);
    },

    // Get all schedules
    getSchedules(startDate = null, endDate = null) {
        return apiClient.get('/api/schedules/', {
            params: { start_date: startDate, end_date: endDate }
        });
    },

    // Get schedule details
    getScheduleDetails(scheduleId) {
        return apiClient.get(`/api/schedules/${scheduleId}`);
    },

    // Assign staff to schedule
    assignStaff(scheduleId, staffIds, notes = null) {
        return apiClient.post('/api/schedules/assign', {
            schedule_id: scheduleId,
            staff_ids: staffIds,
            notes: notes
        });
    },

    // Get staff schedule
    getStaffSchedule(staffId, startDate = null, endDate = null) {
        return apiClient.get(`/api/schedules/staff/${staffId}/schedule`, {
            params: { start_date: startDate, end_date: endDate }
        });
    },

    // Update assignment status
    updateAssignmentStatus(assignmentId, status) {
        return apiClient.patch(`/api/schedules/assignment/${assignmentId}/status`, {
            status: status
        });
    },

    // Export to Excel
    exportToExcel(startDate = null, endDate = null) {
        return apiClient.get('/api/export/excel', {
            params: { start_date: startDate, end_date: endDate },
            responseType: 'blob'
        });
    },

    // Auto-schedule
    autoSchedule(data) {
        return apiClient.post('/api/auto-schedule/generate', data);
    },

    // Get auto-schedule recommendations
    getAutoScheduleRecommendations(days, shiftTypesCount = 1) {
        return apiClient.get('/api/auto-schedule/recommendations', {
            params: { days: days, shift_types_count: shiftTypesCount }
        });
    }
};
