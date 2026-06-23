import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE_URL } from './api.config';

@Injectable({
  providedIn: 'root'
})
export class DriverService {
  private http = inject(HttpClient);
  private apiUrl = `${API_BASE_URL}/api/drivers`;

  getAll(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  getById(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  create(driver: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, driver);
  }

  update(id: number, driver: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, driver);
  }

  delete(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`, { responseType: 'text' as 'json' });
  }
}
