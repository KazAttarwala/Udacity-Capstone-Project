import React, { Component } from 'react'
import axios from 'axios'
import { withAuth0 } from '@auth0/auth0-react';
import getAuthHeader from '../getAuthHeader'
import Error from '../Error'

class UpdateMovie extends Component {
    constructor(props) {
        super(props)

        this.onChangeTitle = this.onChangeTitle.bind(this)
        this.onChangeReleaseDate = this.onChangeReleaseDate.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
        this.onCancelUpdate = this.onCancelUpdate.bind(this)

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

    componentDidMount = async () => {
        const { id } = this.props.match.params;
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "read:movies",
        });

        let me = this;
        axios.get(`/movies/${id}`,
        {headers: {Authorization: `Bearer ${accessToken}`}}).then(response => {
            this.setState({
                title: response.data.movie.title,
                releaseDate: response.data.movie.release_date,
            })
        }).catch(function(error) {
            if (error.response) {
                me.setState({error: error.response.data});
            }
            else {
                alert("Something went wrong! Please try again.")
            }
        });

    }

    onSubmit = async (e) => {
        e.preventDefault()
        const { history } = this.props
        const { id } = this.props.match.params
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "update:movie",
        });

        let movieObj = {
            title: this.state.title,
            release_date: this.state.releaseDate,
        }

        let me = this;
        axios.patch(`/movies/${id}`,
         movieObj,
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

    onCancelUpdate(e) {
        e.preventDefault()

        const { history } = this.props
        history.push('/movies')
    }

    render() {
        let error = this.state.error;
        
        return error ? (<Error error={error} />) : 
        (
            <div className="movie-form" >
                <h3>Update movie</h3>
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
                        <label>Release Date: </label>
                        <input
                            type="date"
                            className="form-control"
                            value={this.state.releaseDate}
                            onChange={this.onChangeReleaseDate}

                        />
                    </div>

                    <div className="form-group">
                        <button onClick={this.onCancelUpdate} className="btn btn-default">Cancel</button>
                        <button type="submit" className="btn btn-success">Update</button>
                    </div>
                </form>
            </div>
        );
    }
}

export default withAuth0(UpdateMovie);