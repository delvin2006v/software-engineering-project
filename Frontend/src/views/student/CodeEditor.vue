<script setup>
import { ref, onMounted } from 'vue';
import { Codemirror } from 'vue-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { oneDark } from '@codemirror/theme-one-dark';

const props = defineProps({
  initialCode: {
    type: String,
    default: '// Write your code here\n'
  }
});

const code = ref(props.initialCode);
const output = ref('');
const isRunning = ref(false);

const extensions = [
  javascript(),
  oneDark
];

const runCode = () => {
  isRunning.value = true;
  output.value = '';
  
  try {
    // Create a safe environment for code execution
    const consoleLogs = [];
    const safeConsole = {
      log: (...args) => consoleLogs.push(args.join(' ')),
      error: (...args) => consoleLogs.push('Error: ' + args.join(' ')),
    };

    // Create a function from the code and execute it with the safe console
    const func = new Function('console', code.value);
    func(safeConsole);
    
    output.value = consoleLogs.join('\n');
  } catch (error) {
    output.value = 'Error: ' + error.message;
  }
  
  isRunning.value = false;
};
</script>

<template>
  <div class="space-y-4">
    <div class="border rounded-lg overflow-hidden">
      <Codemirror
        v-model="code"
        :extensions="extensions"
        :style="{ height: '300px' }"
        class="text-sm"
      />
    </div>
    
    <div class="flex justify-between items-center">
      <button
        @click="runCode"
        :disabled="isRunning"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {{ isRunning ? 'Running...' : 'Run Code' }}
      </button>
    </div>
    
    <div v-if="output" class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
      <h4 class="text-sm font-medium mb-2">Output:</h4>
      <pre class="text-sm whitespace-pre-wrap">{{ output }}</pre>
    </div>
  </div>
</template>