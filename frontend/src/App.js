import React, { Component } from 'react';
import { Route } from 'react-router';
import { Layout } from './components/Layout';
import { Home } from './components/Home';
import Movies from './components/Movie/Movies';
import Actors from './components/Actor/Actors';
import CreateMovie from './components/Movie/CreateMovie';
import CreateActor from './components/Actor/CreateActor';
import UpdateMovie from './components/Movie/UpdateMovie';
import UpdateActor from './components/Actor/UpdateActor';

export default class App extends Component {
  static displayName = App.name;

  render () {
    return (
      <Layout>
        <Route exact path='/' component={Home} />
        <Route path='/actors' component={Actors} />
        <Route path='/movies' component={Movies} />
        <Route path='/add_movie' component={CreateMovie} />
        <Route path='/add_actor' component={CreateActor} />
        <Route path='/update_movie/:id' component={UpdateMovie} />
        <Route path='/update_actor/:id' component={UpdateActor} />
      </Layout>
    );
  }
}
