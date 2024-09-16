// /* eslint-env node */
// require('@rushstack/eslint-patch/modern-module-resolution')

// module.exports = {
//   root: true,
//   'extends': [
//     'plugin:vue/vue3-essential',
//     'eslint:recommended',
//     '@vue/eslint-config-prettier/skip-formatting'
//   ],
//   parserOptions: {
//     ecmaVersion: 'latest'
//   }
// }
/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  env: {
    node: true,  // 添加 Node.js 环境支持
    es6: true    // 支持 ES6 语法
  },
  'extends': [
    'plugin:vue/vue3-essential',  // Vue 3 相关规则
    'eslint:recommended',         // ESLint 推荐规则
    '@vue/eslint-config-prettier/skip-formatting'  // 关闭与 Prettier 冲突的规则
  ],
  parserOptions: {
    ecmaVersion: 'latest'  // 使用最新的 ECMAScript 版本
  }
}
