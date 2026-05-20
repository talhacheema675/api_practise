
from react import useEffect, useState 
from axios import axios 
from lucide-react import  User,Weight,Ruler,MapPin,Trash2,Pencil,Plus,


export default function App() {
  const [patients, setPatients] = useState({});
  const [loading, setLoading] = useState(true);

  const [formData, setFormData] = useState({
    id: "",
    name: "",
    city: "",
    age: "",
    gender: "male",
    height: "",
    weight: "",
  });

  const [editingId, setEditingId] = useState(null);

  const BASE_URL = "http://127.0.0.1:8000";

  // Fetch patients
  const fetchPatients = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${BASE_URL}/view`);
      setPatients(res.data);
    } catch (err) {
      console.log(err);
      alert("Error fetching patients");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  // Handle input
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Create patient
  const createPatient = async () => {
    try {
      await axios.post(`${BASE_URL}/create`, {
        ...formData,
        age: Number(formData.age),
        height: Number(formData.height),
        weight: Number(formData.weight),
      });

      alert("Patient Created");
      resetForm();
      fetchPatients();
    } catch (err) {
      console.log(err);
      alert(err.response?.data?.detail || "Error");
    }
  };

  // Delete patient
  const deletePatient = async (id) => {
    try {
      await axios.delete(`${BASE_URL}/delete/${id}`);
      fetchPatients();
    } catch (err) {
      console.log(err);
    }
  };

  // Edit button click
  const startEdit = (id, patient) => {
    setEditingId(id);

    setFormData({
      id: id,
      name: patient.name,
      city: patient.city,
      age: patient.age,
      gender: patient.gender,
      height: patient.height,
      weight: patient.weight,
    });
  };

  // Update patient
  const updatePatient = async () => {
    try {
      await axios.put(`${BASE_URL}/edit/${editingId}`, {
        ...formData,
        age: Number(formData.age),
        height: Number(formData.height),
        weight: Number(formData.weight),
      });

      alert("Patient Updated");

      setEditingId(null);
      resetForm();
      fetchPatients();
    } catch (err) {
      console.log(err);
      alert("Update failed");
    }
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      id: "",
      name: "",
      city: "",
      age: "",
      gender: "male",
      height: "",
      weight: "",
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto">
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-3xl p-8 text-white shadow-xl">
          <h1 className="text-4xl font-bold">
            Patient Management System
          </h1>
          <p className="mt-2 text-blue-100">
            FastAPI + React + Tailwind CSS
          </p>
        </div>

        {/* Form */}
        <div className="bg-white mt-8 rounded-3xl shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Plus size={24} />
            {editingId ? "Update Patient" : "Add New Patient"}
          </h2>

          <div className="grid md:grid-cols-3 gap-5">
            <input
              type="text"
              name="id"
              placeholder="Patient ID"
              value={formData.id}
              onChange={handleChange}
              disabled={editingId}
              className="border p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              type="text"
              name="name"
              placeholder="Patient Name"
              value={formData.name}
              onChange={handleChange}
              className="border p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              type="text"
              name="city"
              placeholder="City"
              value={formData.city}
              onChange={handleChange}
              className="border p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              type="number"
              name="age"
              placeholder="Age"
              value={formData.age}
              onChange={handleChange}
              className="border p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              type="number"
              name="height"
              placeholder="Height"
              value={formData.height}
              onChange={handleChange}
              className="border p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
            />

            <input
              type="number"
              name="weight"
              placeholder="Weight"
              value={formData.weight}
              onChange={handleChange}
              className="border p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
            />

            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="border p-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="mt-6 flex gap-4">
            {editingId ? (
              <button
                onClick={updatePatient}
                className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-xl font-semibold"
              >
                Update Patient
              </button>
            ) : (
              <button
                onClick={createPatient}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold"
              >
                Create Patient
              </button>
            )}

            <button
              onClick={resetForm}
              className="bg-gray-300 hover:bg-gray-400 px-6 py-3 rounded-xl font-semibold"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Patient Cards */}
        <div className="mt-10">
          <h2 className="text-3xl font-bold mb-6">
            Patients List
          </h2>

          {loading ? (
            <p>Loading...</p>
          ) : (
            <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-6">
              {Object.entries(patients).map(([id, patient]) => (
                <div
                  key={id}
                  className="bg-white rounded-3xl shadow-lg p-6 hover:shadow-2xl transition"
                >
                  <div className="flex justify-between items-center">
                    <h3 className="text-2xl font-bold text-blue-700">
                      {patient.name}
                    </h3>

                    <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">
                      {id}
                    </span>
                  </div>

                  <div className="mt-5 space-y-3">
                    <div className="flex items-center gap-3">
                      <MapPin size={18} />
                      <span>{patient.city}</span>
                    </div>

                    <div className="flex items-center gap-3">
                      <User size={18} />
                      <span>
                        {patient.gender} | {patient.age} yrs
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <Ruler size={18} />
                      <span>{patient.height} cm</span>
                    </div>

                    <div className="flex items-center gap-3">
                      <Weight size={18} />
                      <span>{patient.weight} kg</span>
                    </div>

                    <div className="pt-3">
                      <div className="flex justify-between">
                        <span className="font-semibold">
                          BMI:
                        </span>
                        <span>
                          {patient.calculte?.toFixed(2)}
                        </span>
                      </div>

                      <div className="flex justify-between mt-2">
                        <span className="font-semibold">
                          Verdict:
                        </span>

                        <span
                          className={`font-bold ${
                            patient.calverdict === "overweight"
                              ? "text-red-500"
                              : patient.calverdict === "underweight"
                              ? "text-yellow-500"
                              : "text-green-500"
                          }`}
                        >
                          {patient.calverdict}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-3 mt-6">
                    <button
                      onClick={() => startEdit(id, patient)}
                      className="flex-1 bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-xl flex justify-center items-center gap-2"
                    >
                      <Pencil size={18} />
                      Edit
                    </button>

                    <button
                      onClick={() => deletePatient(id)}
                      className="flex-1 bg-red-500 hover:bg-red-600 text-white py-3 rounded-xl flex justify-center items-center gap-2"
                    >
                      <Trash2 size={18} />
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}