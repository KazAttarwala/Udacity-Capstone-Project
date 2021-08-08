import React, { Component } from 'react';
import axios from 'axios';
import { withAuth0 } from '@auth0/auth0-react';
import Error from '../Error';

class CreateMovie extends Component {

    constructor(props) {
        super(props)

        this.onChangeTitle = this.onChangeTitle.bind(this)
        this.onChangeReleaseDate = this.onChangeReleaseDate.bind(this)
        this.onSubmit = this.onSubmit.bind(this)

        this.state = {
            title: '',
            releaseDate: '',
            error: ''
        }
    }

    onChangeTitle(e) {
        this.setState({
            title: e.target.value
        })
    }

    onChangeReleaseDate(e) {
        this.setState({
            releaseDate: e.target.value
        })
    }

    onSubmit = async (e) => {
        e.preventDefault()
        const {history} = this.props
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "create:movie",
        });

        let movieObject = {
            title: this.state.title,
            release_date: this.state.releaseDate
        }
        
        let me = this;
        axios.post('/movies', 
        movieObject,
        {headers: {Authorization: `Bearer ${accessToken}`}}).then(result => {
            history.push('/movies');
        }).catch(function(error) {
            if (error.response) {
                me.setState({error: error.response.data});
            }
            else {
                alert("Something went wrong! Please try again.")
            }
        });
    }

    render() {
        let error = this.state.error;
        
        return error ? (<Error error={error}/>) : 
        (
            <div className="movie-form" >
                <h3>Add new movie</h3>
                <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label>Title:  </label>
                        <input
                            type="text"
                            className="form-control"
                            value={this.state.title}
                            onChange={this.onChangeTitle}

                        />
                    </div>
                    <div className="form-group">
                        <label>Release date: </label>
                        <input
                            type="date"
                            className="form-control"
                            value={this.state.releaseDate}
                            onChange={this.onChangeReleaseDate}

                        />
                    </div>

                    <div className="form-group">
                        <input type="submit" value="Add movie" className="btn btn-primary" />
                    </div>
                </form>
            </div>
        );
    }
}

export default withAuth0(CreateMovie);
