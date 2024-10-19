import React, { useState } from 'react';
import { createRule } from '../services/api';

const RuleCreator = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [ruleString, setRuleString] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createRule({ name, description, rule_string: ruleString });
      setName('');
      setDescription('');
      setRuleString('');
      alert('Rule created successfully!');
    } catch (error) {
      alert('Error creating rule: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Rule Name"
        required
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Rule Description"
      />
      <textarea
        value={ruleString}
        onChange={(e) => setRuleString(e.target.value)}
        placeholder="Rule String"
        required
      />
      <button type="submit">Create Rule</button>
    </form>
  );
};

export default RuleCreator;