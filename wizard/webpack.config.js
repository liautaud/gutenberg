const path = require('path')
const webpack = require('webpack')

module.exports = {
  entry: [
    './src/index.js',
  ],

  output: {
    path: path.resolve(__dirname, 'static'),
    filename: 'build.js'
  },

  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
    ]
  },

  resolve: {
    extensions: ['*', '.js', '.vue', '.json']
  },

  externals: {
    vue: 'Vue',
  }
}
