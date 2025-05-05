module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_END_POINT,
        changeOrigin: true,
        logLevel: 'info'
      }
    }
  }
}