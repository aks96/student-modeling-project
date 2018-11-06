import React from "react";
import { Switch, Route } from "react-router-dom";

import MainPage from "./MainPage.jsx";
import IssuePage from "./IssuePage.jsx";
import Login from "./Login.jsx";
import Register from "./Register.jsx";
import UserDashboard from "./UserDashboard.jsx";

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.toggleLogin = this.toggleLogin.bind(this);
        this.state = { user: null };
    }

    toggleLogin(user) {
        this.setState({ user });
    }

    render() {
        return (
            <Switch>
                <Route exact path="/" render={(props) =>
                    <MainPage {...props} toggleLogin={this.toggleLogin} />
                } />
                <Route exact path="/dashboard" render={() =>
                    <IssuePage user={this.state.user} toggleLogin={this.toggleLogin} />
                } />
                <Route exact path="/user" render={() =>
                    <UserDashboard user={this.state.user} toggleLogin={this.toggleLogin} />
                } />
                <Route exact path="/login" render={(props) =>
                    <Login {...props} toggleLogin={this.toggleLogin} />
                } />
                <Route exact path="/register" render={(props) =>
                    <Register {...props} toggleLogin={this.toggleLogin} />
                } />
            </Switch>
        );
    }
}

export default Main;
