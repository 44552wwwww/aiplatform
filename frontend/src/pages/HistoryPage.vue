<template>
  <div class="page-container">
    <div class="page-header">
      <h1>我的报告</h1>
    </div>

    <StateWrapper
      :loading="loading"
      :error="error"
      :empty="!loading && reports.length === 0 && !error"
      empty-description="暂无报告，去首页生成吧"
      :retry="fetchList"
    >
      <el-table :data="reports" stripe style="width:100%">
        <el-table-column prop="id" label="#" width="60" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="skill_id" label="类型" width="120" />
        <el-table-column label="时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button size="small" text type="primary" @click="viewReport(row.id)">
              查看
            </el-button>
            <el-button size="small" text type="danger" @click="deleteReport(row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </StateWrapper>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { reportApi, type ReportItem } from '@/api/report'
import { ElMessage, ElMessageBox } from 'element-plus'
import StateWrapper from '@/components/StateWrapper.vue'

const router = useRouter()
const reports = ref<ReportItem[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  await fetchList()
})

async function fetchList() {
  loading.value = true
  error.value = null
  try {
    const res = await reportApi.list()
    reports.value = res.reports
  } catch (e: unknown) {
    error.value = (e as Error).message || '加载报告列表失败'
  } finally {
    loading.value = false
  }
}

function viewReport(id: number) {
  router.push(`/report/${id}`)
}

async function deleteReport(id: number) {
  try {
    await ElMessageBox.confirm('确定删除此报告？', '确认', { type: 'warning' })
  } catch {
    // 取消操作
    return
  }
  try {
    await reportApi.remove(id)
    ElMessage.success('已删除')
    await fetchList()
  } catch (e: unknown) {
    ElMessage.error((e as Error).message || '删除失败')
  }
}

function formatTime(ts: string): string {
  if (!ts) return '-'
  return new Date(ts).toLocaleString('zh-CN')
}
</script>
