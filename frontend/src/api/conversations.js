import {api} from './axios';

export const getConversationsByUser = (userId) => api.get(`conversations/user/${userId}/`);
export const sendChatMessage = (payload) => api.post('conversations/chat/', payload);
