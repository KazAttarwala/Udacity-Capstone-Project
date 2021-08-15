import React, {Component} from 'react'
import axios from 'axios'
import { withAuth0 } from '@auth0/auth0-react';

class Actors extends Component 
{
	constructor(props) {
		super(props)

		this.state =  {
			actors: [],
			loading: true,
			error: ''
		}
	}

	componentDidMount() {
		this.populateActorsData()
	}

	populateActorsData = async () => {
		const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "read:actors",
        });
		
		axios.get('/actors',
		{headers: {Authorization: `Bearer ${accessToken}`}}).then(response => {
			console.log(response.data)
			this.setState({
				actors: response.data.actors,
				loading: false
			})
		})
	}

	redirectToUpdate(actorId) {
		const{history} = this.props;
		history.push(`/update_actor/${actorId}`);
	}

	deleteClicked = async(actorId) => {
		const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "delete:actor",
        });
		
		let me = this;
		axios.delete(`/actors/${actorId}`,
		{headers: {Authorization: `Bearer ${accessToken}`}}).then(response => {
			this.populateActorsData();
		}).catch(function(error) {
            if (error.response) {
                me.setState({error: error.response.data});
            }
            else {
                alert("Something went wrong! Please try again.")
            }
        });
	}

	renderActorsTable(actors) {
		let content = this.state.actors.length <= 0 ? (
			<div>No actors exist yet. Add some!</div>
		) : (
			<table className="table table-striped">
				<thead>
					<tr>
						<th>Name</th>
						<th>Age</th>
						<th>Gender</th>
					</tr>
				</thead>
				<tbody>
					{
						actors.map(actor => (
							<tr key={actor.id}>
								<td>{actor.name}</td>
								<td>{actor.age}</td>
								<td>{actor.gender}</td>
								<td>
                                    <div className="form-group">
                                        <button className="btn btn-primary" onClick={() => this.redirectToUpdate(actor.id)}>Update</button>
                                        <button className="btn btn-danger" onClick={() => this.deleteClicked(actor.id)}>Delete</button>
                                    </div>
                                </td>
							</tr>
						))
					}
				</tbody>
			</table>
		)
		
		return (
			<div>
				{content}
			</div>
		)
	}

	render() {
		let content = this.state.loading ? (
			<p>Loading actors...</p>
		) :
		(
			this.renderActorsTable(this.state.actors)
		)

		if (this.state.error) {
            alert("You do not have permission to delete an actor.");
        }

		return (
			<div>
				<h1>All Actors</h1>
				{content}
			</div>
		)
	}
}

export default withAuth0(Actors);