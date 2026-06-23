import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE_URL } from './api.config';

@Injectable({
  providedIn: 'root'
})
export class TripService {
  private http = inject(HttpClient);
  private apiUrl = `${API_BASE_URL}/api/trips`;

  getTrips(statuses?: string[], startDate?: string): Observable<any[]> {
    let params = new HttpParams();
    if (statuses && statuses.length > 0) {
      // Spring MVC allows binding arrays or collections from comma separated values or repeated parameters.
      // E.g., status=CONCLUIDA,PLANEJADA or status=CONCLUIDA&status=PLANEJADA. Comma joined is cleaner.
      params = params.set('status', statuses.join(','));
    }
    if (startDate) {
      params = params.set('startDate', startDate);
    }
    return this.http.get<any[]>(this.apiUrl, { params });
  }

  getById(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  create(tripRequest: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, tripRequest);
  }

  update(id: number, trip: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, trip);
  }

  delete(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`, { responseType: 'text' as 'json' });
  }
}
