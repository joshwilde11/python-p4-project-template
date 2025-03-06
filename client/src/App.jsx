import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Recipes from './components/Recipes';
import GroceryStoreList from './components/GroceryStoreList';
import DiscountedItems from './components/DiscountedItems';
import RecipeDetail from './components/RecipeDetail';
import Login from './components/login';
import Header from './components/Header';

const PrivateRoute = ({ component: Component, ...rest }) => {
  const isAuthenticated = localStorage.getItem('token');
  return (
    <Route
      {...rest}
      render={props =>
        isAuthenticated ? (
          <Component {...props} />
        ) : (
          <Redirect to="/login" />
        )
      }
    />
  );
};

const App = () => {
  return (
    <Router>
      <Header />
      <Switch>
        <Route path="/login" component={Login} />
        <PrivateRoute path="/grocery-store-list" component={GroceryStoreList} />
        <PrivateRoute path="/discounted-items" component={DiscountedItems} />
        <PrivateRoute path="/recipes/:id" component={RecipeDetail} />
        <PrivateRoute path="/recipes" component={Recipes} />
        <Redirect from="/" to="/login" />
      </Switch>
    </Router>
  );
};

export default App;
