import { createRouter, createWebHistory } from 'vue-router';
import StaffManagement from '../components/StaffManagement.vue';
import ScheduleManagement from '../components/ScheduleManagement.vue';
import StatisticsDashboard from '../components/StatisticsDashboard.vue';

const routes = [
    {
        path: '/',
        redirect: '/statistics'
    },
    {
        path: '/staff',
        name: 'Staff',
        component: StaffManagement
    },
    {
        path: '/schedule',
        name: 'Schedule',
        component: ScheduleManagement
    },
    {
        path: '/statistics',
        name: 'Statistics',
        component: StatisticsDashboard
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
