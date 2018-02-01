const path = require('path');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin')
var webpack = require('webpack')
var config = require("./webpack.config.base")


  config.plugins = config.plugins.concat([
    new UglifyJSPlugin({
      uglifyOptions: {
        sourcemap: false
      }
    })
  ]);

  config.module.loaders.push(
    // { test: /\.jsx?$/, exclude: /node_modules/, loaders: [babel'] }
  )
  // Dev tools are provided by webpack
  // Source maps help map errors to original react code
  // devtool: 'cheap-module-eval-source-map',

module.exports = config
