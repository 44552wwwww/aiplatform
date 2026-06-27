<template>
  <div class="auth-page">
    <el-card class="auth-card">
      <h2>注册 InsightForge</h2>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm">
          <el-input
            v-model="form.confirm"
            type="password"
            placeholder="再次输入密码"
            show-password
            @keyup.enter="handleRegister"
          />
        </el-form-item>
        <el-button
          type="primary"
          :loading="auth.loading"
          native-type="submit"
          style="width:100%"
        >
          注册
        </el-button>
      </el-form>
      <p class="auth-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const auth = useAuthStore()
const router = useRouter()

const formRef = ref<FormInstance>()
const form = reactive({ username: '', password: '', confirm: '' })

const validateConfirm = (_rule: unknown, value: string, callback: (error?: Error) => void) => {
  if (value !== form.password) {
    callback(new Error('两次密码输入不一致'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度 2-50 字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
  ],
  confirm: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' },
  ],
}

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  try {
    await auth.register(form.username, form.password)
    router.push('/')
  } catch (e: unknown) {
    ElMessage.error((e as Error).message || '注册失败')
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px);
  padding: 24px;
}
.auth-card {
  width: 400px;
  max-width: 100%;
}
.auth-card h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #8b4513;
}
.auth-link {
  text-align: center;
  margin-top: 16px;
  color: #909399;
}
.auth-link a {
  color: #8b4513;
}
</style>
