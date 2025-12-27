<template>
  <el-container class="statistics-dashboard">
    <el-header class="page-header">
      <h2>统计分析</h2>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="fetchStatistics"
      />
    </el-header>
    
    <el-main>
      <el-row :gutter="20">
        <!-- Summary Cards -->
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="background: #409eff20">
                <el-icon color="#409eff" :size="40"><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ totalAssignments }}</div>
                <div class="stat-label">总排班次数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="background: #67c23a20">
                <el-icon color="#67c23a" :size="40"><Clock /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ completedCount }}</div>
                <div class="stat-label">已完成班次</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="background: #e6a23c20">
                <el-icon color="#e6a23c" :size="40"><Calendar /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ scheduledCount }}</div>
                <div class="stat-label">待值班次数</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- Workload Table -->
      <el-card style="margin-top: 20px">
        <template #header>
          <div class="card-header">
            <span>人员工作量统计</span>
          </div>
        </template>
        <el-table :data="workloadData" stripe>
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="position" label="职位" />
          <el-table-column prop="shift_count" label="排班次数" sortable>
            <template #default="scope">
              <el-tag type="success">{{ scope.row.shift_count }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- Shift Distribution -->
      <el-card style="margin-top: 20px">
        <template #header>
          <div class="card-header">
            <span>班次分布</span>
          </div>
        </template>
        <el-row :gutter="20">
          <el-col :span="6" v-for="(count, type) in shiftDistribution" :key="type">
            <div class="shift-stat">
              <div class="shift-label">{{ getShiftLabel(type) }}</div>
              <div class="shift-count">{{ count }}</div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { User, Clock, Calendar } from '@element-plus/icons-vue';
import statisticsService from '../api/statisticsService';

export default {
  name: 'StatisticsDashboard',
  components: {
    User,
    Clock,
    Calendar
  },
  setup() {
    const dateRange = ref(null);
    const statisticsData = ref({});
    const workloadData = ref([]);
    const shiftDistribution = ref({});

    const totalAssignments = computed(() => {
      return statisticsData.value.duty_statistics?.total_assignments || 0;
    });

    const completedCount = computed(() => {
      return statisticsData.value.duty_statistics?.status_distribution?.completed || 0;
    });

    const scheduledCount = computed(() => {
      return statisticsData.value.duty_statistics?.status_distribution?.scheduled || 0;
    });

    const fetchStatistics = async () => {
      try {
        let startDate = null;
        let endDate = null;
        
        if (dateRange.value && dateRange.value.length === 2) {
          startDate = dateRange.value[0].toISOString().split('T')[0];
          endDate = dateRange.value[1].toISOString().split('T')[0];
        }

        const response = await statisticsService.getComprehensiveReport(startDate, endDate);
        statisticsData.value = response.data;
        workloadData.value = response.data.staff_workload || [];
        shiftDistribution.value = response.data.shift_distribution || {};
      } catch (error) {
        ElMessage.error('获取统计数据失败');
        console.error(error);
      }
    };

    const getShiftLabel = (type) => {
      const labels = {
        'morning': '早班',
        'afternoon': '中班',
        'night': '晚班'
      };
      return labels[type] || type;
    };

    onMounted(() => {
      fetchStatistics();
    });

    return {
      dateRange,
      totalAssignments,
      completedCount,
      scheduledCount,
      workloadData,
      shiftDistribution,
      fetchStatistics,
      getShiftLabel
    };
  }
};
</script>

<style scoped>
.statistics-dashboard {
  height: 100%;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
}

.shift-stat {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.shift-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.shift-count {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}
</style>
