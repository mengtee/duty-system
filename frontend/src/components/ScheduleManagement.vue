<template>
  <el-container class="schedule-management">
    <el-header class="page-header">
      <h2>排班管理</h2>
      <div class="header-actions">
        <el-button type="success" @click="showAutoScheduleDialog = true">
          <el-icon><MagicStick /></el-icon>
          自动排班
        </el-button>
        <el-button type="warning" @click="handleExport">
          <el-icon><Download /></el-icon>
          导出Excel
        </el-button>
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          创建排班
        </el-button>
      </div>
    </el-header>
    
    <el-main>
      <el-table :data="schedules" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="schedule_date" label="日期" width="150" />
        <el-table-column prop="shift_type" label="班次" width="120">
          <template #default="scope">
            <el-tag>{{ scope.row.shift_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="assignments_count" label="已排人数" width="120" />
        <el-table-column label="排班人员" min-width="220">
          <template #default="scope">
            <span v-if="scope.row.assignments && scope.row.assignments.length > 0" class="staff-names">
              {{ scope.row.assignments.map(a => a.staff?.name || '未知').join(', ') }}
            </span>
            <el-text v-else type="info" size="small">未分配</el-text>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleAssign(scope.row)">
              分配人员
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <!-- Create Schedule Dialog -->
    <el-dialog v-model="showCreateDialog" title="创建排班" width="500">
      <el-form :model="newSchedule" label-width="80px">
        <el-form-item label="日期">
          <el-date-picker
            v-model="newSchedule.schedule_date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="班次">
          <el-select v-model="newSchedule.shift_type" placeholder="选择班次" style="width: 100%">
            <el-option label="早班" value="morning" />
            <el-option label="中班" value="afternoon" />
            <el-option label="晚班" value="night" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">确定</el-button>
      </template>
    </el-dialog>

    <!-- Assign Staff Dialog -->
    <el-dialog v-model="showAssignDialog" title="分配值班人员" width="500">
      <el-form label-width="80px">
        <el-form-item label="选择人员">
          <el-select
            v-model="selectedStaffIds"
            multiple
            placeholder="请选择值班人员"
            style="width: 100%"
          >
            <el-option
              v-for="staff in staffList"
              :key="staff.id"
              :label="`${staff.name} - ${staff.position}`"
              :value="staff.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="assignmentNotes" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAssignDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAssignSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- Auto Schedule Dialog -->
    <el-dialog v-model="showAutoScheduleDialog" title="自动排班" width="600">
      <el-alert
        title="智能排班算法"
        type="info"
        description="系统将根据员工数量自动生成排班，并确保工作量公平分配"
        :closable="false"
        style="margin-bottom: 20px"
      />
      
      <el-form :model="autoScheduleForm" label-width="120px">
        <el-form-item label="起始日期">
          <el-date-picker
            v-model="autoScheduleForm.start_date"
            type="date"
            placeholder="选择起始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker
            v-model="autoScheduleForm.end_date"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="班次类型">
          <el-checkbox-group v-model="autoScheduleForm.shift_types">
            <el-checkbox label="morning">早班</el-checkbox>
            <el-checkbox label="afternoon">中班</el-checkbox>
            <el-checkbox label="night">晚班</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="每班人数">
          <el-input-number v-model="autoScheduleForm.staff_per_shift" :min="1" :max="10" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showAutoScheduleDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAutoSchedule" :loading="autoScheduling">
          生成排班
        </el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Download, MagicStick } from '@element-plus/icons-vue';
import scheduleService from '../api/scheduleService';
import staffService from '../api/staffService';

export default {
  name: 'ScheduleManagement',
  components: {
    Plus,
    Download,
    MagicStick
  },
  setup() {
    const schedules = ref([]);
    const staffList = ref([]);
    const loading = ref(false);
    const showCreateDialog = ref(false);
    const showAssignDialog = ref(false);
    const showAutoScheduleDialog = ref(false);
    const autoScheduling = ref(false);
    const selectedSchedule = ref(null);
    const selectedStaffIds = ref([]);
    const assignmentNotes = ref('');
    
    const newSchedule = ref({
      schedule_date: new Date(),
      shift_type: 'morning'
    });

    const autoScheduleForm = ref({
      start_date: new Date(),
      end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
      shift_types: ['morning', 'afternoon'],
      staff_per_shift: 2
    });

    const fetchSchedules = async () => {
      loading.value = true;
      try {
        const response = await scheduleService.getSchedules();
        schedules.value = response.data;
      } catch (error) {
        ElMessage.error('获取排班列表失败');
        console.error(error);
      } finally {
        loading.value = false;
      }
    };

    const fetchStaff = async () => {
      try {
        const response = await staffService.getAllStaff();
        staffList.value = response.data;
      } catch (error) {
        console.error(error);
      }
    };

    const handleCreate = async () => {
      try {
        const data = {
          schedule_date: newSchedule.value.schedule_date.toISOString().split('T')[0],
          shift_type: newSchedule.value.shift_type
        };
        await scheduleService.createSchedule(data);
        ElMessage.success('创建成功');
        showCreateDialog.value = false;
        fetchSchedules();
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '创建失败');
      }
    };

    const handleAssign = (schedule) => {
      selectedSchedule.value = schedule;
      selectedStaffIds.value = [];
      assignmentNotes.value = '';
      showAssignDialog.value = true;
    };

    const handleAssignSubmit = async () => {
      if (selectedStaffIds.value.length === 0) {
        ElMessage.warning('请至少选择一名人员');
        return;
      }
      
      try {
        await scheduleService.assignStaff(
          selectedSchedule.value.id,
          selectedStaffIds.value,
          assignmentNotes.value
        );
        ElMessage.success('分配成功');
        showAssignDialog.value = false;
        fetchSchedules();
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '分配失败');
      }
    };

    const handleAutoSchedule = async () => {
      if (!autoScheduleForm.value.start_date || !autoScheduleForm.value.end_date) {
        ElMessage.warning('请选择起始和结束日期');
        return;
      }

      if (autoScheduleForm.value.shift_types.length === 0) {
        ElMessage.warning('请至少选择一个班次类型');
        return;
      }

      try {
        await ElMessageBox.confirm(
          '自动排班将生成新的排班记录，确定要继续吗？',
          '确认自动排班',
          { type: 'warning' }
        );

        autoScheduling.value = true;
        const response = await scheduleService.autoSchedule({
          start_date: autoScheduleForm.value.start_date.toISOString().split('T')[0],
          end_date: autoScheduleForm.value.end_date.toISOString().split('T')[0],
          shift_types: autoScheduleForm.value.shift_types,
          staff_per_shift: autoScheduleForm.value.staff_per_shift
        });

        ElMessage.success(
          `自动排班成功！生成了 ${response.data.summary.total_schedules} 个排班，` +
          `${response.data.summary.total_assignments} 个分配`
        );
        showAutoScheduleDialog.value = false;
        fetchSchedules();
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error(error.response?.data?.detail || '自动排班失败');
        }
      } finally {
        autoScheduling.value = false;
      }
    };

    const handleExport = async () => {
      try {
        ElMessage.info('正在生成Excel文件...');
        const response = await scheduleService.exportToExcel();
        
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `schedule_export_${Date.now()}.xlsx`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        
        ElMessage.success('导出成功');
      } catch (error) {
        ElMessage.error('导出失败');
        console.error(error);
      }
    };

    onMounted(() => {
      fetchSchedules();
      fetchStaff();
    });

    return {
      schedules,
      staffList,
      loading,
      showCreateDialog,
      showAssignDialog,
      showAutoScheduleDialog,
      autoScheduling,
      newSchedule,
      selectedStaffIds,
      assignmentNotes,
      autoScheduleForm,
      handleCreate,
      handleAssign,
      handleAssignSubmit,
      handleAutoSchedule,
      handleExport
    };
  }
};
</script>

<style scoped>
.schedule-management {
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

.header-actions {
  display: flex;
  gap: 10px;
}

.staff-names {
  color: #606266;
  font-size: 14px;
}
</style>
