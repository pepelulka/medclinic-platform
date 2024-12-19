import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AppointmentsLogs = () => {
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchLogs = async (page, limit) => {
    setLoading(true);
    try {
      const skip = (page - 1) * limit
      const response = await axios.get(
        `http://localhost/api/appointments_logs?skip=${skip}&limit=${limit}`
      );
      setLogs(response.data.logs);
      setTotal(response.data.total);
      console.log(logs)
    } catch (error) {
      console.error("Error fetching logs:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs(page, limit);
  }, [page, limit]);

  const handleLimitChange = (e) => {
    setLimit(Number(e.target.value));
    setPage(1); // Reset to the first page on limit change
  };

  const totalPages = Math.ceil(total / limit);

  const myToLocaleString = (str) => {
    return new Date(str).toLocaleString()
  }

  const eventTypeTranslate = {
    create: 'Создание',
    cancel: 'Отмена'
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Журнал записей</h1>

      <div style={{ marginBottom: '10px' }}>
        <label htmlFor="limit">Записей на странице: </label>
        <select id="limit" value={limit} onChange={handleLimitChange}>
          <option value={5}>5</option>
          <option value={10}>10</option>
          <option value={20}>20</option>
          <option value={50}>50</option>
        </select>
      </div>

      {loading ? (
        <p>Загрузка...</p>
      ) : (
        <table border="1" style={{ width: '100%', borderCollapse: 'collapse' }} className='[&>*]:border-black [&>*]:border-2'>
          <thead>
            <tr className='[&>*]:border-black [&>*]:border-2'>
              <th>ID пациента</th>
              <th>Имя пациента</th>
              <th>ID записи</th>
              <th>Время записи</th>
              <th>Время события</th>
              <th>ID Врача</th>
              <th>Имя врача</th>
              <th>Адрес клиники</th>
              <th>Событие</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={`${log.appointment_id}-${log.time}`} className='[&>*]:border-black [&>*]:border-2 [&>*]:p-2'>
                <td>{log.patient_id}</td>
                <td>{log.patient_name}</td>
                <td>{log.appointment_id}</td>
                <td>{myToLocaleString(log.appointment_time)}</td>
                <td>{myToLocaleString(log.event_time)}</td>
                <td>{log.doctor_id}</td>
                <td>{log.doctor_name}</td>
                <td>{log.clinic_address}</td>
                <td>{eventTypeTranslate[log.event_type]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div style={{ marginTop: '10px', display: 'flex', justifyContent: 'space-between' }}>
        <button
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </button>

        <span>
          Page {page} of {totalPages}
        </span>

        <button
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={page === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default AppointmentsLogs;
