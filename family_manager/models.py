from django.db import models

class Family(models.Model):
    name = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200, verbose_name="Address 1", blank=True)
    address2 = models.CharField(max_length=200, verbose_name="Address 2", blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    anniversary = models.DateField(verbose_name="Anniversary Date", blank=True, null=True)
    indexed_name = models.CharField(max_length=500, editable=False)

    def get_displayable_name(self):
        primaries = self.familymember_set.filter(member_type__lte=3).order_by("name_sort") # Gets primary types
        primary_count = primaries.count()
        primary_names = ""

        for i in range(0, primary_count):
            if i < primary_count - 1 or primary_count == 1:
                prefix = ", "
            elif i > 1:
                prefix = ", and "
            else:
                prefix = " and "

            primary_names += prefix + primaries[i].get_singular_name()

        return self.name + primary_names

    def members_with_phones(self):
        return self.familymember_set.exclude(phone="")

    def members_with_email(self):
        return self.familymember_set.exclude(email="")

    def save(self, expected_name=None):
        if expected_name is None:
            expected_name = self.get_displayable_name()
            
        if self.indexed_name != expected_name:
            self.indexed_name = expected_name

        super(Family, self).save()

    class Meta:
               verbose_name_plural = "Families"

    def __unicode__(self):
        return self.indexed_name

class FamilyMember(models.Model):

    MEMBER_TYPE_CHOICES = (
        (1, 'Husband/Father'),
        (2, 'Wife/Mother'),
        (3, 'Other Primary'),
        (4, 'Daughter'),
        (5, 'Son')
    )

    family = models.ForeignKey(Family)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, default=family.name, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    email = models.EmailField(verbose_name="E-Mail", blank=True)
    phone = models.CharField(max_length=13, blank=True)
    member_type = models.IntegerField(choices=MEMBER_TYPE_CHOICES, blank=True, null=True)
    name_sort = models.IntegerField(editable=False)

    def save(self):
        if self.last_name == "" :
            self.last_name = self.family.name

        if self.last_name == self.family.name:
            self.name_sort = 0
        else:
            self.name_sort = 1

        super(FamilyMember, self).save()

        new_family_name = self.family.get_displayable_name()

        if self.family.indexed_name != new_family_name:
            self.family.indexed_name = new_family_name
            self.family.save(expected_name=new_family_name)

    def delete(self):
        super(FamilyMember, self).delete()

        new_family_name = self.family.get_displayable_name()

        if self.family.indexed_name != new_family_name:
            self.family.indexed_name = new_family_name
            self.family.save(expected_name=new_family_name)

    def get_singular_name(self):
        if self.last_name == self.family.name :
            return self.first_name
        else :
            return self.__unicode__()

    def __unicode__(self):
        return self.last_name + ", " + self.first_name