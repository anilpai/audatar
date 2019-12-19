// Original code from https://github.com/gaearon/react-document-title

var React = require('react'),
  PropTypes = require('prop-types'),
  withSideEffect = require('react-side-effect')

function reducePropsToState(propsList) {
  var innermostProps = propsList[propsList.length - 1]
  if (innermostProps) {
    return innermostProps.title
  }
}

function handleStateChangeOnClient(title) {
  var nextTitle = title || ''
  if (nextTitle !== document.title) {
    document.title = nextTitle ? nextTitle + ' | Audatar' : 'Audatar'
  }
}

function BasePage() {}

BasePage.prototype = Object.create(React.Component.prototype)

BasePage.displayName = 'BasePage'
BasePage.propTypes = {
  title: PropTypes.string.isRequired,
  style: PropTypes.object
}

BasePage.prototype.render = function() {
  if (this.props.children) {
    return (
      <div className="panel panel-default" style={this.props.style}>
        <div className="panel-heading">
          <p className="panel-title">{this.props.title}</p>
        </div>
        <section className="panel-body" id="body">
          {React.Children.only(this.props.children)}
        </section>
      </div>
    )
  } else {
    return null
  }
}

module.exports = withSideEffect(reducePropsToState, handleStateChangeOnClient)(
  BasePage
)
