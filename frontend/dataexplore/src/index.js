import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home'; // example component
import About from './components/About'; // example component
import App from './App'; // Assuming App is defined in a separate file

// Define the App component
function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/about" component={About} />
      </Switch>
    </Router>
  );
}

// Render the App component
ReactDOM.render(<App />, document.getElementById('root'));
