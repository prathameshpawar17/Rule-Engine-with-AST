import React from 'react';
import RuleCreator from './components/RuleCreator';
import RuleList from './components/RuleList';
import RuleEvaluator from './components/RuleEvaluator';
import RuleCombiner from './components/RuleCombiner';
import RuleModifier from './components/RuleModifier';

function App() {
  return (
    <div className="App">
      <h1>Rule Engine Application</h1>
      <div className="container">
        <div className="column">
          <h2>Create Rule</h2>
          <RuleCreator />
        </div>
        <div className="column">
          <h2>Rule List</h2>
          <RuleList />
        </div>
      </div>
      <div className="container">
        <div className="column">
          <h2>Evaluate Rule</h2>
          <RuleEvaluator />
        </div>
        <div className="column">
          <h2>Combine Rules</h2>
          <RuleCombiner />
        </div>
      </div>
      <div className="container">
        <div className="column">
          <h2>Modify Rule</h2>
          <RuleModifier />
        </div>
      </div>
    </div>
  );
}

export default App;