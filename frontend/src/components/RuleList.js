import React, { useState, useEffect } from 'react';
import { getRules } from '../services/api';

const RuleList = () => {
  const [rules, setRules] = useState([]);

  useEffect(() => {
    const fetchRules = async () => {
      try {
        const fetchedRules = await getRules();
        setRules(fetchedRules);
      } catch (error) {
        console.error('Error fetching rules:', error);
      }
    };
    fetchRules();
  }, []);

  return (
    <ul>
      {rules.map((rule) => (
        <li key={rule.id}>
          <strong>{rule.name}</strong>: {rule.description}
        </li>
      ))}
    </ul>
  );
};

export default RuleList;