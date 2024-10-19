import React, { useState } from 'react';
import { modifyRule } from '../services/api';

const RuleModifier = () => {
  const [ruleId, setRuleId] = useState('');
  const [path, setPath] = useState('');
  const [newValue, setNewValue] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const pathArray = path.split('.').filter(Boolean);
      await modifyRule(ruleId, pathArray, newValue);
      alert('Rule modified successfully!');
    } catch (error) {
      alert('Error modifying rule: ' + error.message);
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
      <input
        type="text"
        value={path}
        onChange={(e) => setPath(e.target.value)}
        placeholder="Path (e.g., left.right.value)"
        required
      />
      <input
        type="text"
        value={newValue}
        onChange={(e) => setNewValue(e.target.value)}
        placeholder="New Value"
        required
      />
      <button type="submit">Modify Rule</button>
    </form>
  );
};

export default RuleModifier;