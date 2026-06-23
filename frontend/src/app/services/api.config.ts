import { isDevMode } from '@angular/core';

export const API_BASE_URL = isDevMode()
  ? 'http://localhost:8081'
  : 'https://fleet-management-api.vercel.app';
