// Original code from https://stackoverflow.com/a/36222827

import * as loglevel from 'loglevel'

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
  loglevel.setLevel('debug')
} else {
  loglevel.setLevel('error')
}

export default loglevel
