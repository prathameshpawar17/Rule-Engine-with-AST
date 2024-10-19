import React, { useState } from 'react';
import { combineRules } from '../services/api';

const RuleCombiner = () => {
  const [ruleIds, setRuleIds] = useState('');
  const [combinedRule, setCombinedRule] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const ids = ruleIds.split(',').map(id => parseInt(id.trim()));
      const result = await combineRules(ids);
      setCombinedRule(result);
    } catch (error) {
      alert('Error combining rules: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={ruleIds}
        onChange={(e) => setRuleIds(e.target.value)}
        placeholder="Rule IDs (comma-separated)"
        required
      />
      <button type="submit">Combine Rules</button>
      {combinedRule && (
        <div>
          <h3>Combined Rule:</h3>
          <pre>{JSON.stringify(combinedRule, null, 2)}</pre>
        </div>
      )}
    </form>
  );
};

export default RuleCombiner;