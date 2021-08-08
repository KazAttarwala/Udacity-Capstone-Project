import React, { Component } from 'react'
import axios from 'axios'
import { withAuth0 } from '@auth0/auth0-react';
import getAuthHeader from '../getAuthHeader';

class UpdateActor extends Component {
    constructor(props) {
        super(props)

        this.onChangeName = this.onChangeName.bind(this)
        this.onChangeGender = this.onChangeGender.bind(this)
        this.onChangeAge = this.onChangeAge.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
        this.onCancelUpdate = this.onCancelUpdate.bind(this)

        this.state = {
            name: '',
            age: 0,
            gender: ''
        }
    }

    onChangeName(e) {
        this.setState({
            name: e.target.value
        });
    }

    onChangeGender(e) {
        this.setState({
            gender: e.target.value
        });
    }

    onChangeAge(e) {
        this.setState({
            age: e.target.value
        });
    }

    componentDidMount = async () => {
        const { id } = this.props.match.params
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "read:actors",
        });

        axios.get(`/actors/${id}`,
        {headers: {Authorization: `Bearer ${accessToken}`}}).then(response => {
            this.setState({
                name: response.data.actor.name,
                gender: response.data.actor.gender,
                age: response.data.actor.age
            });
        })

    }

    onSubmit = async (e) => {
        e.preventDefault()
        const { history } = this.props
        const { id } = this.props.match.params
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "update:actor",
        });

        let actorObj = {
            name: this.state.name,
            gender: this.state.gender,
            age: this.state.age
        }

        axios.patch(`/actors/${id}`, 
        actorObj,
        {headers: {Authorization: `Bearer ${accessToken}`}}).then(result => {
            history.push('/actors');
        })
    }

    onCancelUpdate(e) {
        e.preventDefault()

        const { history } = this.props
        history.push('/actors')
    }

    render() {
        return (
            <div className="movie-form" >
                <h3>Update actor</h3>
                <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label>Name:  </label>
                        <input
                            type="text"
                            className="form-control"
                            value={this.state.name}
                            onChange={this.onChangeName}

                        />
                    </div>
                    <div className="form-group">
                        <label>Gender: </label>
                        <select className="form-select" aria-label="Gender" value={this.state.gender} onChange={this.onChangeGender}>
                            <option selected></option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label>Age: </label>
                        <input
                            type="text"
                            className="form-control"
                            value={this.state.age}
                            onChange={this.onChangeAge}
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

export default withAuth0(UpdateActor);