watch('.*\.(py|html|txt)') do |match_data_object|
  system('python setup.py install --force')
  system('cd test_project && python manage.py test --noinput --with-sneazr')
end
