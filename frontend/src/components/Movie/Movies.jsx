import React, {Component} from 'react'
import axios from 'axios'
import { withAuth0 } from '@auth0/auth0-react';

class Movies extends Component 
{
	constructor(props) {
		super(props)

		this.state =  {
			movies: [],
			loading: true
		}
	}

	componentDidMount() {
		this.populateMoviesData()
	}

	populateMoviesData = async () => {
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "read:movies",
        });
        
        axios.get('/movies',
        {headers: {Authorization: `Bearer ${accessToken}`}}).then(response => {
			this.setState({
				movies: response.data.movies,
				loading: false
			})
		})
    }

    redirectToUpdate(movidId) {
        const {history} = this.props;
        history.push(`/update_movie/${movidId}`);
    }

    deleteClicked = async (movieId) => {
        const { getAccessTokenSilently } = this.props.auth0;
        const domain = "https://localhost:5000";
        const accessToken = await getAccessTokenSilently({
            audience: domain,
            scope: "delete:movie",
        });
        
        axios.delete(`/movies/${movieId}`,
        {headers: {Authorization: `Bearer ${accessToken}`}}).then(response => {
            this.populateMoviesData();
        })
    }

	renderMoviesTable(movies) {
		return (
			<table className="table table-striped">
				<thead>
					<tr>
						<th>Title</th>
						<th>Release Date</th>
					</tr>
				</thead>
				<tbody>
					{
						movies.map(movie => (
							<tr key={movie.id}>
								<td>{movie.title}</td>
								<td>{new Date(movie.release_date).toLocaleDateString()}</td>
                                <td>
                                    <div className="form-group">
                                        <button className="btn btn-primary" onClick={() => this.redirectToUpdate(movie.id)}>Update</button>
                                        <button className="btn btn-danger" onClick={() => this.deleteClicked(movie.id)}>Delete</button>
                                    </div>
                                </td>
							</tr>
						))
					}
				</tbody>
			</table>
		)
	}

	render() {
		let content = this.state.loading ? (
			<p>Loading movies...</p>
		) :
		(
			this.renderMoviesTable(this.state.movies)
		)

		return (
			<div>
				<h1>All Movies</h1>
				{content}
			</div>
		)
	}
}

export default withAuth0(Movies);