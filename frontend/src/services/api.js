import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const createRule = async (ruleData) => {
  const response = await axios.post(`${API_URL}/rules/`, ruleData);
  return response.data;
};

export const getRules = async () => {
  const response = await axios.get(`${API_URL}/rules/`);
  return response.data;
};

export const evaluateRule = async (ruleId, userData) => {
  const response = await axios.post(`${API_URL}/rules/${ruleId}/evaluate`, { data: userData });
  return response.data;
};

export const combineRules = async (ruleIds) => {
  const response = await axios.post(`${API_URL}/rules/combine`, { rule_ids: ruleIds });
  return response.data;
};

export const modifyRule = async (ruleId, path, newValue) => {
  const response = await axios.put(`${API_URL}/rules/${ruleId}/modify`, { path, new_value: newValue });
  return response.data;
};