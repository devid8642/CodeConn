function my_scope() {
  const forms = document.querySelectorAll('.form-delete');

  for (const form of forms) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const confirmed = confirm('Tem certeza de que deseja deletar este item?');

      if (confirmed) {
        form.submit();
      }
    });
  }
}

function complaint() {
  const forms = document.querySelectorAll('.form-complaint');

  for (const form of forms) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const confirmed = confirm('Tem certeza de que deseja denunciar este post?');

      if (confirmed) {
        form.submit();
      }
    });
  }
}

my_scope();
complaint();
