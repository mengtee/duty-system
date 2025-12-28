<template>
  <el-container class="staff-management">
    <el-header class="page-header">
      <h2>值班人员管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加人员
      </el-button>
    </el-header>
    
    <el-main>
      <el-table :data="staffList" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" min-width="120" />
        <el-table-column prop="age" label="年龄" width="100" />
        <el-table-column prop="position" label="职位" min-width="150" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <!-- Add Staff Dialog -->
    <el-dialog v-model="showAddDialog" title="添加值班人员" width="500">
      <el-form :model="newStaff" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="newStaff.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="年龄">
          <el-input-number v-model="newStaff.age" :min="18" :max="100" />
        </el-form-item>
        <el-form-item label="职位">
          <el-input v-model="newStaff.position" placeholder="请输入职位" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确定</el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import staffService from '../api/staffService';

export default {
  name: 'StaffManagement',
  components: {
    Plus
  },
  setup() {
    const staffList = ref([]);
    const loading = ref(false);
    const showAddDialog = ref(false);
    const newStaff = ref({
      name: '',
      age: 25,
      position: ''
    });

    const fetchStaff = async () => {
      loading.value = true;
      try {
        const response = await staffService.getAllStaff();
        staffList.value = response.data;
      } catch (error) {
        ElMessage.error('获取人员列表失败');
        console.error(error);
        staffList.value = [];
      } finally {
        loading.value = false;
      }
    };

    const handleAdd = async () => {
      try {
        await staffService.createStaff(newStaff.value);
        ElMessage.success('添加成功');
        showAddDialog.value = false;
        newStaff.value = { name: '', age: 25, position: '' };
        fetchStaff();
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '添加失败');
      }
    };

    const handleDelete = async (staff) => {
      try {
        await ElMessageBox.confirm(`确定要删除 ${staff.name} 吗？`, '确认删除', {
          type: 'warning'
        });
        await staffService.deleteStaff(staff.id);
        ElMessage.success('删除成功');
        fetchStaff();
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败');
        }
      }
    };

    onMounted(() => {
      fetchStaff();
    });

    return {
      staffList,
      loading,
      showAddDialog,
      newStaff,
      handleAdd,
      handleDelete
    };
  }
};
</script>

<style scoped>
.staff-management {
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
</style>
