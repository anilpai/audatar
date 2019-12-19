import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Control, actions } from 'react-redux-form'
import {TAGS} from './tags'
import './Tag.css'
import { WithContext as ReactTags } from 'react-tag-input'

const mapTags = function(tags) {
  if(!tags) return [];
  return tags.split(',').map((tag) => {
    return {
      id: tag.trim(),
      text: tag.trim()
    }
  })
}

const suggestions = TAGS.map((tag) => {
  return {
    id: tag,
    text: tag
  }
})

const KeyCodes = {
  comma: 188,
  enter: 13,
};

const delimiters = [KeyCodes.comma, KeyCodes.enter]


class TagInput extends React.Component {
  constructor(props){
    super(props)
    this.generateTagsString = this.generateTagsString.bind(this)
    this.handleDelete = this.handleDelete.bind(this)
    this.handleAddition = this.handleAddition.bind(this)
    this.handleDrag = this.handleDrag.bind(this)
    this.handleTagClick = this.handleTagClick.bind(this)
  }

  handleDelete(i) {
    const { tags } = this.props;
    this.props.onChange &&
      this.props.onChange(this.generateTagsString(tags.filter((tag, index) => index !== i)));
  }

  handleAddition(tag) {
     const { tags } = this.props;
     this.props.onChange &&
      this.props.onChange(this.generateTagsString([...tags, tag]))
  }

  handleDrag(tag, currPos, newPos) {
    const tags = [...this.props.tags]
    const newTags = tags.slice()

    newTags.splice(currPos, 1)
    newTags.splice(newPos, 0, tag)

    this.props.onChange &&
      this.props.onChange(this.generateTagsString([...newTags]))
  }

  generateTagsString(t){
    let tags = []
       for (let i=0;i<t.length;i++) {
            tags.push(t[i].id)
         }
    return tags.join(",")
}

  handleTagClick(index) {
    console.log('The tag at index ' + index + ' was clicked')
    console.log(this.state.tags)
  }

  render() {
    const { tags } = this.props;
  return (
     <div
       className={`form-group row ${
         this.props.valid === false ? 'has-error' : ''
       }`}
     >
       <div className="col-sm-2">
         <label
           htmlFor={this.props.name}
           className="col-form-label control-label"
         >
           {this.props.label || this.props.name}
         </label>
       </div>
       <div className="col-sm-10">
       <ReactTags
         tags={this.props.tags}
         suggestions={suggestions}
         delimiters={delimiters}
         handleDelete={this.handleDelete}
         handleAddition={this.handleAddition}
         handleDrag={this.handleDrag}
         handleTagClick={this.handleTagClick}
       />
       </div>
       <div>
        <br/>
       </div>
     </div>
   )
 }
}

TagInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func,
  includeAllOption: PropTypes.bool
}


const mapStateToProps = state => {
  return {
    tags: state.validationcheckform && mapTags(state.validationcheckform.tags) || ''
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      idChange: (model, id) => actions.change(model, id)
    },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(TagInput)
