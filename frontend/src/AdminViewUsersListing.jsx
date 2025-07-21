import { useContext, useState } from "react";
import { AuthContext } from "./App";

export default function AdminViewUsersListing({
  username,
  role,
  userId,
  onChange
}) {
  const [loading, setLoading] = useState(false);
  const { setAuthenticated, accessToken } = useContext(AuthContext);

  function changeRoles(userId, newRole) {
    setLoading(true);
    fetch(
      "http://localhost:8000/api/admin/role?" + new URLSearchParams({
        user_id: userId,
        new_role: newRole
      }),
      {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      }
    )
    .then(function(_) {
      onChange();
    })
    .catch(function(error) {
      console.log(error)
      setAuthenticated(false);
    })
    .finally(function() {
      setLoading(false);
    })
  }

  const availableRoles = ["User", "Mod", "Admin"]
  const role_switch_buttons = availableRoles
      .filter(roleListItem => roleListItem !== role)
      .map(roleListItem => {
        return (
          <button
            key={roleListItem}
            onClick={() => changeRoles(userId, roleListItem)}
            disabled={loading}
          >
            Switch to {roleListItem}
          </button>
        );
      });

  return (
    <li data-user-id={userId} >
      <h3>{username} ({role}) {role_switch_buttons}</h3>
    </li>
  );

}
