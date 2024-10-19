import React, { useState } from 'react';
import { evaluateRule } from '../services/api';

const RuleEvaluator = () => {
  const [ruleId, setRuleId] = useState('');
  const [userData, setUserData] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = JSON.parse(userData);
      const evaluationResult = await evaluateRule(ruleId, data);
      setResult(evaluationResult.result);
    } catch (error) {
      alert('Error evaluating rule: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="number"
        value={ruleId}
        onChange={(e) => setRuleId(e.target.value)}
        placeholder="Rule ID"
        required
      />
      <textarea
        value={userData}
        onChange={(e) => setUserData(e.target.value)}
        placeholder="User Data (JSON format)"
        required
      />
      <button type="submit">Evaluate Rule</button>
      {result !== null && (
        <div>
          Result: {result ? 'True' : 'False'}
        </div>
      )}
    </form>
  );
};

export default RuleEvaluator;