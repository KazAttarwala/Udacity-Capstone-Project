import React, { Component } from 'react';
import axios from 'axios';
import { withAuth0 } from '@auth0/auth0-react';
import Error from '../Error'

export class CreateActor extends Component {

    constructor(props) {
        super(props)

        this.onChangeName = this.onChangeName.bind(this)
        this.onChangeGender = this.onChangeGender.bind(this)
        this.onChangeAge = this.onChangeAge.bind(this)
        this.onSubmit = this.onSubmit.bind(this)

        this.state = {
            name: '',
            gender: '',
            age: '',
            error: ''
        }
    }

    onChangeName(e) {
        this.setState({
            name: e.target.value
        })
    }

    onChangeGender(e) {
        this.setState({
            gender: e.target.value
        })
    }

    onChangeAge(e) {
        this.setState({
            age: e.target.value
        })
    }

    onSubmit = async (e) => {
        e.preventDefault()
        const {history} = this.props
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "create:actor",
        });

        let actorObject = {
            name: this.state.name,
            age: this.state.age,
            gender: this.state.gender
        }

        let me = this;
        axios.post('/actors', 
        actorObject, 
        {headers: {Authorization: `Bearer ${accessToken}`}}).then(result => {
            history.push('/actors');
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
            <div className="actor-form" >
                <h3>Add new actor</h3>
                <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label>Name: </label>
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
                        <input type="submit" value="Add actor" className="btn btn-primary" />
                    </div>
                </form>
            </div>
        );
    }
}

export default withAuth0(CreateActor);
