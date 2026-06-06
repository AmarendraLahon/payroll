/* Assam Government University — Payroll & Leave Demo
   Vanilla JS only. No frameworks, no build, no fetch (works from file://).
   Responsibilities: shared top-nav injection, login role handling,
   pay-matrix render, tabs, table filtering, mock leave-apply. */

(function () {
  "use strict";

  // ---- Page registry (single source of nav truth) ----
  var PAGES = [
    { href: "dashboard.html",      label: "Dashboard" },
    { href: "employee.html",       label: "Employee" },
    { href: "payslip.html",        label: "Payslip" },
    { href: "pay-matrix.html",     label: "Pay Matrix" },
    { href: "leave.html",          label: "Leave" },
    { href: "increment-macp.html", label: "Increment / MACP" },
    { href: "arrears.html",        label: "Arrears" },
    { href: "loans.html",          label: "Loans" },
    { href: "claims.html",         label: "Claims" },
    { href: "salary-bill.html",    label: "Salary Bill" },
    { href: "pension.html",        label: "Pension" },
    { href: "reports.html",        label: "Reports" },
    { href: "admin.html",          label: "Admin / RBAC" }
  ];

  function currentFile() {
    var p = location.pathname.split("/").pop();
    return p || "dashboard.html";
  }

  // ---- Indian number format helper ----
  function inr(n) {
    return "₹" + Number(n).toLocaleString("en-IN");
  }
  window.inr = inr;

  // ---- Build the shared top nav into <nav class="topnav" id="topnav"> ----
  function buildNav() {
    var nav = document.getElementById("topnav");
    if (!nav) return;
    var here = currentFile();
    var inner = document.createElement("div");
    inner.className = "inner";
    PAGES.forEach(function (pg) {
      var a = document.createElement("a");
      a.href = pg.href;
      a.textContent = pg.label;
      if (pg.href === here) a.className = "active";
      inner.appendChild(a);
    });
    var out = document.createElement("a");
    out.href = "login.html";
    out.textContent = "Logout";
    out.className = "logout";
    inner.appendChild(out);
    nav.appendChild(inner);
  }

  // ---- Reflect selected role (from login) in the header "who" area ----
  function showRole() {
    var who = document.getElementById("who-role");
    if (!who) return;
    var role = "";
    try { role = localStorage.getItem("agu_role") || ""; } catch (e) {}
    if (role) who.textContent = role;
  }

  // ---- Role → per-role workflow folder ----
  var ROLE_HOME = {
    "Employee":          "employee/index.html",
    "Dealing Assistant": "dealing-assistant/index.html",
    "DDO":               "ddo/index.html",
    "Approver":          "approver/index.html",
    "Auditor":           "auditor/index.html",
    "Admin":             "admin/index.html"
  };

  // ---- Login page: remember role, go to that role's workflow home ----
  function wireLogin() {
    var form = document.getElementById("login-form");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var sel = document.getElementById("role");
      var role = sel ? sel.value : "Employee";
      try { localStorage.setItem("agu_role", role); } catch (err) {}
      location.href = ROLE_HOME[role] || "dashboard.html";
    });
  }

  // ---- Pay Matrix render (7th CPC: cell = prev x 1.03, round up to next 100) ----
  function buildMatrix() {
    var host = document.getElementById("matrix");
    if (!host) return;
    // entry pay (cell 1) per level — illustrative state 7th-CPC / Assam ROP shape
    var entry = {
      1: 18000, 2: 19900, 3: 21700, 4: 23900, 5: 29200,
      6: 35400, 7: 44900, 8: 47600, 9: 53100, 10: 56100
    };
    var CELLS = 12;
    // Mr. Das sits at Level 4 / Cell 3 (Basic 25,500); Mr. Roy at Level 10 / Cell 1.
    var marks = { "4-3": true, "10-1": true };

    function row(level) {
      var cells = [entry[level]];
      for (var c = 1; c < CELLS; c++) {
        cells.push(Math.ceil((cells[c - 1] * 1.03) / 100) * 100);
      }
      return cells;
    }

    var thead = "<thead><tr><th class='lvl'>Level \\ Cell</th>";
    for (var c = 1; c <= CELLS; c++) thead += "<th class='num'>" + c + "</th>";
    thead += "</tr></thead>";

    var tbody = "<tbody>";
    Object.keys(entry).forEach(function (lvl) {
      tbody += "<tr><th class='lvl'>Level " + lvl + "</th>";
      row(+lvl).forEach(function (val, i) {
        var key = lvl + "-" + (i + 1);
        var cls = "num" + (marks[key] ? " matrix-cell highlight" : "");
        tbody += "<td class='" + cls + "'>" + Number(val).toLocaleString("en-IN") + "</td>";
      });
      tbody += "</tr>";
    });
    tbody += "</tbody>";

    host.innerHTML = thead + tbody;
  }

  // ---- Simple tabs: buttons with data-tab -> panes with id ----
  function wireTabs() {
    var groups = document.querySelectorAll(".tabs");
    groups.forEach(function (g) {
      g.querySelectorAll("button[data-tab]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var target = btn.getAttribute("data-tab");
          g.querySelectorAll("button").forEach(function (b) { b.classList.remove("active"); });
          btn.classList.add("active");
          // panes share a common parent ancestor — search whole document by id list
          var ids = (btn.getAttribute("data-group") || "").split(",");
          document.querySelectorAll(".tabpane").forEach(function (p) {
            if (p.getAttribute("data-group") === btn.getAttribute("data-group")) {
              p.classList.toggle("active", p.id === target);
            }
          });
        });
      });
    });
  }

  // ---- Table filter: input[data-filter="tableId"] filters rows by text ----
  function wireFilters() {
    document.querySelectorAll("[data-filter]").forEach(function (inp) {
      inp.addEventListener("input", function () {
        var tbl = document.getElementById(inp.getAttribute("data-filter"));
        if (!tbl) return;
        var q = inp.value.toLowerCase();
        tbl.querySelectorAll("tbody tr").forEach(function (tr) {
          tr.style.display = tr.textContent.toLowerCase().indexOf(q) > -1 ? "" : "none";
        });
      });
    });
  }

  // ---- Mock "Apply Leave" form (leave.html) ----
  function wireLeaveForm() {
    var form = document.getElementById("leave-form");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var type = document.getElementById("lv-type").value;
      var from = document.getElementById("lv-from").value;
      var to = document.getElementById("lv-to").value;
      var days = document.getElementById("lv-days").value || "1";
      var tbody = document.querySelector("#leave-applied tbody");
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" + (from || "—") + " to " + (to || "—") + "</td>" +
        "<td>" + type + "</td>" +
        "<td class='num'>" + days + "</td>" +
        "<td><span class='badge warn'>Pending — HOD</span></td>";
      tbody.insertBefore(tr, tbody.firstChild);
      var msg = document.getElementById("leave-msg");
      if (msg) {
        msg.style.display = "block";
        msg.textContent = "Mock application submitted. Routed to approval workflow: Employee → HOD → Registrar. (No data is saved.)";
      }
      form.reset();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    buildNav();
    showRole();
    wireLogin();
    buildMatrix();
    wireTabs();
    wireFilters();
    wireLeaveForm();
  });
})();
