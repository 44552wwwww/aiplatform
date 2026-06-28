<template>
  <!-- Priority: loading > error > empty > content -->
  <LoadingSpinner v-if="loading" :size="spinnerSize" class="py-16" />
  <ErrorAlert v-else-if="error" :message="error" :retry="retry" />
  <EmptyState v-else-if="empty" :description="emptyDescription" />
  <slot v-else />
</template>

<script setup lang="ts">
import LoadingSpinner from './LoadingSpinner.vue'
import ErrorAlert from './ErrorAlert.vue'
import EmptyState from './EmptyState.vue'

withDefaults(defineProps<{
  loading: boolean
  error: string | null
  empty: boolean
  emptyDescription?: string
  retry?: () => void
  spinnerSize?: 'sm' | 'default' | 'lg'
}>(), {
  spinnerSize: 'default',
})
</script>
