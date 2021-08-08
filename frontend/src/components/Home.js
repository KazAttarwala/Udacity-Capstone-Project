import React, { Component } from 'react';

export class Home extends Component {
  static displayName = Home.name;

  render () {
    return (
      <div>
        <h1>Welome to the ChiTown Casting Manager</h1>
        <p>Interact with the manager by: </p>
        <ul>
            <li>Getting all actors</li>
            <li>Creating an actor</li>
            <li>Updating/Deleting an actor</li>
            <li>Getting all movies</li>
            <li>Creating a movie</li>
            <li>Updating/Deleting a movie</li>
        </ul>
      </div>
    );
  }
}
