import React, { Component } from 'react';
import { Collapse, Container, Nav, Navbar, NavbarBrand, NavbarToggler, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';
import './NavMenu.css';
import LoginButton from './LoginButton';
import { withAuth0 } from '@auth0/auth0-react';

class NavMenu extends Component {
  static displayName = NavMenu.name;

  constructor (props) {
    super(props);

    this.state = {
      
    };
  }

  render () {
    const {isAuthenticated, logout} = this.props.auth0;

    let navItems = isAuthenticated ? (
      <ul className="navbar-nav flex-grow">
        <NavItem>
          <NavLink tag={Link} className="text-dark" to="/actors">Actors</NavLink>
        </NavItem>
        <NavItem>
          <NavLink tag={Link} className="text-dark" to="/movies">Movies</NavLink>
        </NavItem>
        <NavItem>
          <NavLink tag={Link} className="text-dark" to="/add_actor">Add actor</NavLink>
        </NavItem>
        <NavItem>
          <NavLink tag={Link} className="text-dark" to="/add_movie">Add movie</NavLink>
        </NavItem>
        <NavItem>
          <button onClick={() => logout()}class="btn btn-danger">Log Out</button>
        </NavItem>
      </ul>
    ) : (
      <ul className="navbar-nav flex-grow">
        <LoginButton />
      </ul>
    )
    
    return (
      <header>
        <Navbar className="navbar-expand-sm navbar-toggleable-sm ng-white border-bottom box-shadow mb-3" light>
          <Container>
            <NavbarBrand tag={Link} to="/">ChiTown Casting</NavbarBrand>
              {navItems}
          </Container>
        </Navbar>
      </header>
    );
  }
}

export default withAuth0(NavMenu);
