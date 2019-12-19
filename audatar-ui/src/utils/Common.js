export function getDeepProp(obj, props, valueIfNotFound = null) {
  var paths = props.split('.'),
    current = obj,
    i

  for (i = 0; i < paths.length; ++i) {
    if (current[paths[i]] == null) {
      return valueIfNotFound
    } else {
      current = current[paths[i]]
    }
  }

  return current || valueIfNotFound
}
